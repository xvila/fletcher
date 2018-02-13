from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Line
from bokeh.embed import components
from statsmodels.nonparametric.smoothers_lowess import lowess
import seaborn as sns
import matplotlib.pyplot as plt, mpld3
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = 12, 6

app = Flask(__name__)

# Load the Iris Data Set
df = pd.read_pickle('data/sentiment.pkl')
feature_names = df.title.unique().tolist()
feature_names = sorted(feature_names)

# Create the main plot
def create_figure(current_feature_name,df,f=.1,d=0.0):
    bookDF = df.loc[df['title']==current_feature_name]
    sentiment=list(bookDF.sentiment)
    lowX=list(range(1,len(sentiment)+1))
    low_plot=lowess(sentiment,lowX,frac=.1,return_sorted=False,delta=d)
    fig = plt.figure()
    plt.plot(low_plot,label=current_feature_name)
    plt.ylabel("Sentiment Score")
    plt.xlabel("Sentence #")
    plt.title(current_feature_name)    
    plt.legend()
    p =  mpld3.fig_to_html(fig)
    # #Set the x axis label
    # p.xaxis.axis_label=current_feature_name
    # #Set the y axis label
    # p.yaxis.axis_label='Sentiment'
    return p

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Cujo"

	# Create the plot
	plot = create_figure(current_feature_name,df)
		
	# Embed plot into HTML via Flask Render
	return render_template("index.html",plot=plot,feature_names=feature_names,current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)