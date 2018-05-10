function getSampleNames() {
  let selector = document.getElementById('selectedDataset');
  let url = "/names";
  Plotly.d3.json(url, function(error, response) {
    if(error) return console.warn(error);
    let data = response;
    data.map(function(sample) {
      let option = document.createElement('option')
      option.text = sample
      option.value = sample
      selector.appendChild(option)
    });
  });
};

getSampleNames();

function optionChanged(sample) {
  updatePie(sample);
  updateBubble(sample);
  updateMetadata(sample);
};

function updatePie(sample) {
  let sampleURL = `/samples/${sample}`
  Plotly.d3.json(sampleURL, function(error, response) {
    if (error) return console.log(error);
    let labels = []
    let values = []
    let hovers = []
    for (i = 0; i < 10; i++) {
      let label = response[0].otu_ids[i];
      labels.push(label);
      let value = response[1].sample_values[i];
      values.push(value);
      let hover = response[2][label - 1];
      hovers.push(hover);
    };
    let trace = {
      values: values,
      labels: labels,
      type: "pie",
      text: hovers,
      hoverinfo: "label+text+value+percent",
      textinfo: "percent"
    };
    let data = [trace]
    let layout = {
      margin: {
        l: 10,
        r: 10,
        h: 10,
        t: 10,
        pad: 4
      }
    }

    Plotly.newPlot("pieChart", data, layout)
  });
};

function updateBubble(sample) {
  let sampleURL = `/samples/${sample}`
  Plotly.d3.json(sampleURL, function(error, response) {
    if (error) return console.log(error);
    let otuIDs = response[0].otu_ids;
    let sampleValues = response[1].sample_values
    let otuDescriptions = [];
    for (i = 0; i < otuIDs.length; i++) {
      otuDescriptions.push(response[2][otuIDs[i] - 1]);
    };
    let trace = {
      x: otuIDs,
      y: sampleValues,
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: sampleValues,
        color: otuIDs,
        colorscale: "Rainbow"
      },
      text: otuDescriptions
    };
    let data = [trace]
    Plotly.newPlot("bubbleChart", data)
  });
};

function updateMetadata(sample) {
  let sampleURL = `/metadata/${sample}`
  Plotly.d3.json(sampleURL, function(error, response) {
    if (error) return console.log(error);
    console.log(response);
    let data = response[0];
    console.log(data)
    let metaList = document.getElementById('sampleMetadata');
    metaList.innerHTML = '';
    let metaItems = [["Sample", "SAMPLEID"], ["Ethnicity", "ETHNICITY"], ["Gender", "GENDER"], ["Age", "AGE"],
    ["Weekly Wash Frequency", "WFREQ"], ["Type (Innie/Outie)", "BBTYPE"], ["Country", "COUNTRY012"], ["Dog Owner", "DOG"], ["Cat Owner", "CAT"]];
    console.log(metaList)
    for (i = 0; i < metaItems.length; i++) {
      let newLi = document.createElement('li');
      newLi.innerHTML = `${metaItems[i][0]}: ${data[metaItems[i][1]]}`;
      metaList.appendChild(newLi);
    };
  });
};

optionChanged("BB_940")