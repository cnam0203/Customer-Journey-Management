from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .forms import formContact
from .models import Touchpoint
from .models import Graph
from datetime import datetime
import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.process_tree import converter as pt_converter

from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization




@user_passes_test(lambda user: user.is_staff)
def private_place(request):
    return HttpResponse("Shhh, members only!", content_type="text/plain")

# Create your views here.

@user_passes_test(lambda user: user.is_staff)
def home(request):
    return render(request, "home/index.html")

@user_passes_test(lambda user: user.is_staff)
def importData(request):
    return render(request, "home/import-data.html")

@user_passes_test(lambda user: user.is_staff)
def exportData(request):
    return render(request, "home/visualize-graph.html")


@user_passes_test(lambda user: user.is_staff)
def classifyTouchpoint(request):
    return 'Classify Touchpoint'


@user_passes_test(lambda user: user.is_staff)
def predictTouchpoint(request):
    return 'Predict Touchpoint'


@user_passes_test(lambda user: user.is_staff)
def clusterJourney(request):
    return render(request, "home/cluster-journey.html")


@user_passes_test(lambda user: user.is_staff)
def automationRule(request):
    return 'Automation Rules'


@user_passes_test(lambda user: user.is_staff)
def visualizeGraph(request):
    return render(request, "home/visualize-graph.html", {"imgSrc": ''})


@user_passes_test(lambda user: user.is_staff)
def getGraph(request):
    if (request.method == "POST"):
        startDate = datetime(2000, 1, 1)
        endDate = datetime.now()
        type = request.POST["algorithm"]
        if (request.POST["startDate"] != ''):
            startDate = request.POST["startDate"]
        if (request.POST["endDate"] != ''):
            endDate = request.POST["endDate"]
        touchpoints = Touchpoint.objects.filter(visit_time__range=[startDate, endDate]).values('user_id', 'visit_time', 'active_time', 'action_type')
        touchpoints = list(touchpoints)

        graph = processMining(touchpoints, type)
        graphLink = saveGraph(graph, startDate, endDate, type)
        return render(request, "home/visualize-graph.html", {"imgSrc": graphLink})


@user_passes_test(lambda user: user.is_staff)
def getCluster(request):
    if (request.method == "POST"):
        startDate = datetime(2000, 1, 1)
        endDate = datetime.now()

        numClusters = int(request.POST["numClusters"])
        algorithm = request.POST["algorithmMethod"]
        preprocess = request.POST["preprocessMethod"]

        if (request.POST["startDate"] != ''):
            startDate = request.POST["startDate"]
        if (request.POST["endDate"] != ''):
            endDate = request.POST["endDate"]
        touchpoints = Touchpoint.objects.filter(visit_time__range=[startDate, endDate]).values('user_id', 'visit_time', 'active_time', 'action_type')
        touchpoints = list(touchpoints)

        user_journeys, user_ids = create_journey(touchpoints)
        list_action_types = get_list_action_types(touchpoints)
        x_data = preprocessTouchpoint(user_journeys, list_action_types, preprocess)

        clusters, predict_journeys = cluster_touchpoints(x_data, algorithm, numClusters)
        list_clustered_touchpoints = [[] for i in range(0, len(clusters))]

        for index, user_id in enumerate(user_ids):
            cluster_index = predict_journeys[index]
            user_touchpoints = [touchpoint for touchpoint in touchpoints if touchpoint["user_id"] == user_id]
            list_clustered_touchpoints[cluster_index] = list_clustered_touchpoints[cluster_index] + user_touchpoints
            
        graphLinks = []
        for clustered_touchpoint in list_clustered_touchpoints:
            graph = processMining(clustered_touchpoint, "dfg-discovery-frequency")
            graphLink = saveGraph(graph, startDate, endDate, "dfg-discovery-frequency")
            graphLinks.append(graphLink)

        return render(request, "home/cluster-journey.html", {"graphLinks": graphLinks})


@user_passes_test(lambda user: user.is_staff)
def uploadFile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        touchpoints = body['data']
        for touchpoint in touchpoints:
            new_touchpoint = Touchpoint.objects.create()
            for key in touchpoint:
                setattr(new_touchpoint, key, touchpoint[key])
            new_touchpoint.save()
        return JsonResponse({"result": "Import Successfully"})


def get_list_action_types(touchpoints):
    df = pd.DataFrame(touchpoints)
    list_action_types = df["action_type"].unique()
    return list_action_types

def create_journey(touchpoints):
    df = pd.DataFrame(touchpoints)
    list_journeys = []
    list_userID = df["user_id"].unique()
    for userID in list_userID:
        user_journey = df.loc[df["user_id"]==userID, ["action_type", "visit_time"]]
        user_journey = user_journey.sort_values(['visit_time'], ascending=[True])
        user_journey = user_journey["action_type"].tolist()
        list_journeys.append(user_journey)

    return list_journeys, list_userID


def cluster_touchpoints(x_data, algorithm, numClusters):
    clusters = np.array([])
    predict_journeys = np.array([])
    if (algorithm == "kmeans"):
        clusters, predict_journeys = kmeans_clustering(x_data, numClusters)
    return clusters, predict_journeys


def kmeans_clustering(x_data, numClusters):
    kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(x_data)
    predict_journeys = kmeans.predict(x_data)
    return kmeans.cluster_centers_, predict_journeys


def preprocessTouchpoint(user_journeys, list_action_types, preprocess):
    preprocessed_touchpoints = np.array([])
    if (preprocess == "bagOfActivities"):
        preprocessed_touchpoints = preprocess_bag_of_activities(user_journeys, list_action_types)
    if (preprocess == "sequenceVector"):
        preprocessed_touchpoints = preprocess_sequence_vector(user_journeys, list_action_types)
    return preprocessed_touchpoints

def preprocess_bag_of_activities(user_journeys, list_action_types):
    list_touchpoint_vectors = []
    for journey in user_journeys:
        touchpoint_vector = []
        for action_type in list_action_types:
            touchpoint_vector.append(journey.count(action_type))
        list_touchpoint_vectors.append(touchpoint_vector)

    return list_touchpoint_vectors


def preprocess_sequence_vector(touchpoints, list_action_types):
    return None


def processMining(touchpoints, type):
    df = pd.DataFrame(touchpoints)
    df["visit_time"] = pd.to_datetime(df['visit_time'], unit='s')
    df = dataframe_utils.convert_timestamp_columns_in_df(df)
    df.rename(columns={'user_id':'case:concept:name', 'action_type':'concept:name', 'visit_time':'time:timestamp'}, inplace=True)
    df = df.sort_values(by=['case:concept:name','time:timestamp'])
    log = log_converter.apply(df)
    
    gviz = None 
    
    if type == "alpha":
        gviz = alphaMiner(log)
    elif type == "heuristic":
        gviz = heuristicMiner(log)
    elif type == "dfg-discovery-frequency":
        gviz = dfgDiscoveryFrequency(log)
    elif type == "dfg-discovery-active-time":
        gviz = dfgDiscoveryActiveTime(log)
    elif type == "inductive-miner-tree":
        gviz = InductiveMinerTree(log)
    elif type == "inductive-miner-petri":
        gviz = InductiveMinerPetriNet(log)
    
    return gviz

def alphaMiner(log):
    # alpha miner
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz

def heuristicMiner(log):
    # heuristic miner
    net, initial_marking, final_marking = heuristics_miner.apply(log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz

def dfgDiscoveryActiveTime(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
    gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
    return gviz

def dfgDiscoveryFrequency(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log)
    gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
    return gviz

def InductiveMinerTree(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    gviz = pt_visualizer.apply(tree)
    return gviz

def InductiveMinerPetriNet(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    # convert the process tree to a petri net
    net, initial_marking, final_marking = pt_converter.apply(tree)
    parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, 
                           parameters=parameters, 
                           variant=pn_visualizer.Variants.FREQUENCY, 
                           log=log)
    return gviz

def saveGraph(gviz, startDate, endDate, type):
    filename = '/graph/' + str(datetime.now().timestamp()) + ".png"
    path = "home/static" + filename
    staticPath = 'http://localhost:8000/static' + filename 
    pn_visualizer.save(gviz, path)
    newGraph = Graph.objects.create(runDate=datetime.now(), startDate=startDate, endDate=endDate, type=type, link=staticPath)
    newGraph.save()

    return filename
    







    



