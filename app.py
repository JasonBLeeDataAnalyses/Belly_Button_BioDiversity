# Import Statements
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
  Flask,
  render_template,
  jsonify,
  request,
  redirect)

# open Flask
app = Flask(__name__)

# database setup
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect = True)
Sample = Base.classes.samples
OTU = Base.classes.otu
Metadata = Base.classes.samples_metadata

session = Session(engine)

# Creating routes
@app.route("/")
def home():
  return render_template("index.html")

@app.route('/names')
def names():
  tot_samples = session.query(Sample).statement
  tot_samples_df = pd.read_sql_query(tot_samples, session.bind)
  tot_samples_df.set_index('otu_id', inplace = True)
  return jsonify(list(tot_samples_df.columns))

@app.route('/otu')
def otu():
  tot_otus = session.query(OTU).statement
  tot_otus_df = pd.read_sql_query(tot_otus, session.bind)
  tot_otus_df.set_index('otu_id', inplace = True)
  return jsonify(list(tot_otus_df["lowest_taxonomic_unit_found"]))

@app.route('/metadata/<sample>')
def metadata(sample):
  tot_samples_metadata = session.query(Metadata).statement
  tot_samples_metadata_df = pd.read_sql_query(tot_samples_metadata, session.bind)
  sample_num = int(sample.split("_")[1])
  selected_sample = tot_samples_metadata_df.loc[tot_samples_metadata_df["SAMPLEID"] == sample_num, :]
  json_selected_sample = selected_sample.to_json(orient = 'records')
  return json_selected_sample

@app.route('/wfreq/<sample>')
def wfreq(sample):
  tot_samples_metadata = session.query(Metadata).statement
  tot_samples_metadata_df = pd.read_sql_query(tot_samples_metadata, session.bind)
  sample_num = int(sample.split("_")[1])
  selected_sample = tot_samples_metadata_df.loc[tot_samples_metadata_df["SAMPLEID"] == sample_num, :]
  wfreq = selected_sample["WFREQ"].values[0]
  return f"{wfreq}"

@app.route('/samples/<sample>')
def samples(sample):
  tot_otus = session.query(OTU).statement
  tot_otus_df = pd.read_sql_query(tot_otus, session.bind)
  tot_otus_df.set_index('otu_id', inplace = True)

  tot_samples = session.query(Sample).statement
  tot_samples_df = pd.read_sql_query(tot_samples, session.bind)
  selected_sample = tot_samples_df[sample]
  otu_ids = tot_samples_df['otu_id']
  selection_df = pd.DataFrame({
    "otu_ids": otu_ids,
    "samples": selected_sample
  })
  sorted_df = selection_df.sort_values(by = ['samples'], ascending= False)
  sorted_otus = {"otu_ids": list(sorted_df['otu_ids'].values)}
  sorted_samples = {"sample_values": list(sorted_df['samples'].values)}
  for i in range(len(sorted_otus["otu_ids"])):
    sorted_otus["otu_ids"][i] = int(sorted_otus["otu_ids"][i])
  for i in range(len(sorted_samples["sample_values"])):
    sorted_samples["sample_values"][i] = int(sorted_samples["sample_values"][i])
  results = [sorted_otus, sorted_samples, list(tot_otus_df["lowest_taxonomic_unit_found"])]
  return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)