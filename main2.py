from pm4pymdl.objects.mdl.importer import importer as mdl_importer
from pm4pymdl.objects.sqlite.importer import importer as sqlite_importer
from pm4pymdl.objects.ocel.importer import importer as ocel_importer
from pm4pymdl.algo.mvp.get_logs_and_replay import algorithm as discovery_factory
from pm4pymdl.visualization.petrinet import visualizer as pn_vis_factory
import pandas as pd
import pm4py
#df = mdl_importer.apply("./example_logs/mdl/order_management.mdl")
#df = sqlite_importer.apply("./my_data/p2p/ocel2-p2p.sqlite")
eve_df, obj_df = ocel_importer.apply("./my_data/recruiting.jsonocel")
#eve_df, obj_df = ocel_importer.apply("./my_data/github_pm4py.json")


model = discovery_factory.apply(eve_df)
gviz = pn_vis_factory.apply(model, parameters={"format": "svg"})
pn_vis_factory.view(gviz)
