from pm4pymdl.objects.mdl.importer import importer as mdl_importer
from pm4pymdl.algo.mvp.gen_framework import algorithm as discovery
from pm4pymdl.visualization.mvp.gen_framework import visualizer as vis_factory
import pandas as pd

df_offer = mdl_importer.apply("../example_logs/parquet/bpic2017_offer.parquet")
df_offer["event_idx_log_0"] = df_offer.index
df_offer = df_offer.sort_values(["event_timestamp", "event_idx_log_0"])
df_application = mdl_importer.apply("../example_logs/parquet/bpic2017_application.parquet")
df_application["event_idx_log_0"] = df_application.index
df_application = df_application.sort_values(["event_timestamp", "event_idx_log_0"])
#df_application.fillna(value=pd.np.nan, inplace=True)
df = pd.concat([df_offer, df_application])
df["event_idx_log"] = df.index
df = df.reset_index()
df = df.sort_values(["event_timestamp", "event_idx_log"])
df.drop(columns="index", inplace=True)
model = discovery.apply(df)
gviz = vis_factory.apply(model, parameters={"dfg_cleaning_threshold": 0.15, "max_edge_ratio": 0.99, "format": "svg"})
vis_factory.view(gviz)
