import json

from flask import Flask, render_template
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components

app = Flask(__name__)

@app.route("/")
def index():
    # df = pd.read_pickle('sentiment.pkl')
#     chart_data = df.to_dict(orient='records')
#     chart_data = json.dumps(chart_data, indent=2)
#     data = {'chart_data': chart_data}
#     return render_template("index.html", data=data)
    name = request.args.get("name")
	if name == None:
		name = "Edward"
	return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run(port=5000,debug=True)