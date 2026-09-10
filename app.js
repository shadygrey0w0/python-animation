const lessons={
python:{
label:"PYTHON BASICS",
title:"Python Basics",
description:"Learn the Python concepts you need before working with data.",
items:[
{
title:"Variables",
description:"Store values using simple variable names.",
intro:"Variables let us give names to values.",
explanation:"A variable is a name that refers to a value. Python can store numbers, text, and many other types of data.",
code:`name="Alice"
age=20
score=85

print(name)
print(age)
print(score)`,
output:`Alice
20
85`,
key:"A variable stores a value that we can use later."
},
{
title:"Lists",
description:"Store several values together.",
intro:"Lists are useful when we have a collection of values.",
explanation:"A Python list can contain several values. Lists are useful for storing collections of data.",
code:`scores=[72,85,91,68,88]

for score in scores:
    print(score)`,
output:`72
85
91
68
88`,
key:"Python lists use square brackets and start counting at index 0."
},
{
title:"Loops",
description:"Repeat an operation for every value.",
intro:"Loops help us work through data one value at a time.",
explanation:"A for loop repeats code for each item in a collection.",
code:`scores=[70,80,90]

for score in scores:
    print(score)`,
output:`70
80
90`,
key:"A loop lets us perform the same operation on many values."
},
{
title:"Conditions",
description:"Make decisions using if statements.",
intro:"Conditions allow programs to make decisions.",
explanation:"The if statement runs code when a condition is true.",
code:`score=82

if score>=50:
    print("Pass")
else:
    print("Fail")`,
output:"Pass",
key:"Use if and else when your program needs to make a decision."
},
{
title:"Functions",
description:"Create reusable pieces of code.",
intro:"Functions help us organize repeated calculations.",
explanation:"A function is a reusable block of code.",
code:`def average(a,b):
    return (a+b)/2

result=average(80,90)

print(result)`,
output:"85.0",
key:"Functions package logic into reusable pieces."
}
]
},
numpy:{
label:"NUMPY",
title:"NumPy Basics",
description:"Use NumPy arrays for numerical calculations.",
items:[
{
title:"Create an Array",
description:"Turn Python values into a NumPy array.",
intro:"NumPy arrays are a basic building block for numerical data.",
explanation:"NumPy provides the array structure used heavily in scientific computing.",
code:`import numpy as np

x=np.array([10,20,30,40])

print(x)`,
output:"[10 20 30 40]",
key:"A NumPy array stores numerical values in an efficient structure."
},
{
title:"Array Calculations",
description:"Perform calculations on an entire array.",
intro:"NumPy lets us calculate with many values at once.",
explanation:"NumPy can apply an operation to an entire array.",
code:`import numpy as np

x=np.array([10,20,30,40])

print(x*2)
print(x+5)`,
output:`[20 40 60 80]
[15 25 35 45]`,
key:"NumPy operations can work across an entire array."
},
{
title:"Mean, Min and Max",
description:"Calculate simple statistics with NumPy.",
intro:"NumPy includes useful statistical functions.",
explanation:"Mean gives the average. Min gives the smallest value and max gives the largest.",
code:`import numpy as np

scores=np.array([60,70,80,90,100])

print(np.mean(scores))
print(np.min(scores))
print(np.max(scores))`,
output:`80.0
60
100`,
key:"Mean, minimum, and maximum summarize numerical data."
},
{
title:"Array Shape",
description:"Understand array dimensions.",
intro:"Shape tells us how an array is organized.",
explanation:"A two-dimensional array can be thought of as rows and columns.",
code:`import numpy as np

data=np.array([
    [10,20],
    [30,40],
    [50,60]
])

print(data.shape)`,
output:"(3, 2)",
key:"Shape tells us the number of rows and columns."
},
{
title:"Indexing",
description:"Access individual values in an array.",
intro:"Indexing lets us select specific values.",
explanation:"NumPy uses zero-based indexing. The first element has index 0.",
code:`import numpy as np

x=np.array([10,20,30,40])

print(x[0])
print(x[2])`,
output:`10
30`,
key:"The first element is at index 0."
}
]
},
pandas:{
label:"PANDAS",
title:"Pandas Basics",
description:"Organize, inspect, filter, and summarize data using Pandas.",
items:[
{
title:"Create a DataFrame",
description:"Build a simple table from Python data.",
intro:"A Pandas DataFrame is like a table of data.",
explanation:"DataFrames organize information into rows and columns.",
code:`import pandas as pd

data={
    "Name":["Ana","Ben","Cara"],
    "Score":[80,90,75]
}

df=pd.DataFrame(data)

print(df)`,
output:`   Name  Score
0   Ana     80
1   Ben     90
2  Cara     75`,
key:"A DataFrame represents data as rows and columns."
},
{
title:"Select a Column",
description:"Work with one column.",
intro:"Selecting a column is a common Pandas operation.",
explanation:"We can select a column using its name inside square brackets.",
code:`import pandas as pd

df=pd.DataFrame({
    "Name":["Ana","Ben","Cara"],
    "Score":[80,90,75]
})

print(df["Score"])`,
output:`0    80
1    90
2    75`,
key:"Use df['ColumnName'] to select a column."
},
{
title:"Filter Rows",
description:"Find rows that satisfy a condition.",
intro:"Filtering lets us select only the data we want.",
explanation:"Pandas can use a condition to select matching rows.",
code:`import pandas as pd

df=pd.DataFrame({
    "Name":["Ana","Ben","Cara"],
    "Score":[80,90,75]
})

high=df[df["Score"]>=80]

print(high)`,
output:`  Name  Score
0  Ana     80
1  Ben     90`,
key:"Filtering lets us work with a subset of data."
},
{
title:"Head",
description:"Look at the first rows.",
intro:"The head() method gives us a quick look at our data.",
explanation:"When working with a large dataset, we often inspect the first few rows.",
code:`import pandas as pd

df=pd.DataFrame({
    "Age":[18,21,25,30,35],
    "Score":[70,82,91,76,88]
})

print(df.head(3))`,
output:`   Age  Score
0   18     70
1   21     82
2   25     91`,
key:"head() is a quick way to inspect a DataFrame."
},
{
title:"Describe",
description:"Get a statistical summary.",
intro:"describe() gives useful summary statistics.",
explanation:"The describe() method summarizes numerical columns.",
code:`import pandas as pd

df=pd.DataFrame({
    "Score":[60,70,80,90,100]
})

print(df.describe())`,
output:`       Score
count    5.0
mean    80.0
min     60.0
max    100.0`,
key:"describe() gives a quick statistical overview."
}
]
},
statistics:{
label:"STATISTICAL LEARNING",
title:"Statistical Learning",
description:"Use simple statistics to understand patterns in data.",
items:[
{
title:"Mean",
description:"Find the average value.",
intro:"The mean summarizes the center of numerical data.",
explanation:"The mean is calculated by adding all values and dividing by the number of values.",
code:`import numpy as np

x=np.array([10,20,30,40,50])

print(np.mean(x))`,
output:"30.0",
key:"Mean = sum of values divided by the number of values."
},
{
title:"Variance",
description:"Measure how spread out values are.",
intro:"Variance tells us how much values vary around their mean.",
explanation:"A small variance means values stay closer to the mean. A larger variance means they are more spread out.",
code:`import numpy as np

x=np.array([10,20,30,40,50])

print(np.var(x))`,
output:"200.0",
key:"Variance measures the spread of numerical values."
},
{
title:"Correlation",
description:"Explore how two variables move together.",
intro:"Correlation describes the strength and direction of a linear relationship.",
explanation:"A correlation close to 1 means two variables tend to increase together.",
code:`import numpy as np

hours=np.array([1,2,3,4,5])
scores=np.array([50,60,70,80,90])

r=np.corrcoef(hours,scores)[0,1]

print(round(r,2))`,
output:"1.0",
key:"Correlation describes the direction and strength of a linear relationship."
},
{
title:"Simple Regression",
description:"Predict one variable from another.",
intro:"Linear regression fits a straight line to data.",
explanation:"A regression line describes the relationship between an input variable and an output variable.",
code:`import numpy as np

x=np.array([1,2,3,4,5])
y=np.array([2,4,6,8,10])

slope,intercept=np.polyfit(x,y,1)

print("Slope:",slope)
print("Intercept:",intercept)`,
output:`Slope: 2.0
Intercept: 0.0`,
key:"Linear regression finds a line that describes the relationship between variables."
}
]
}
};

let currentTopic="python";
let currentLesson=0;

function showHome(){
document.getElementById("home-view").classList.remove("hidden");
document.getElementById("topic-view").classList.add("hidden");
document.getElementById("lesson-view").classList.add("hidden");
window.scrollTo(0,0);
}

function openTopic(topic){
currentTopic=topic;
const data=lessons[topic];

document.getElementById("topic-label").textContent=data.label;
document.getElementById("topic-title").textContent=data.title;
document.getElementById("topic-description").textContent=data.description;

renderLessons();

document.getElementById("home-view").classList.add("hidden");
document.getElementById("topic-view").classList.remove("hidden");
document.getElementById("lesson-view").classList.add("hidden");

window.scrollTo(0,0);
}

function renderLessons(){
const grid=document.getElementById("lesson-grid");
grid.innerHTML="";

lessons[currentTopic].items.forEach((lesson,index)=>{
const card=document.createElement("button");

card.className="lesson-card";

card.innerHTML=`
<span class="lesson-number">LESSON ${String(index+1).padStart(2,"0")}</span>
<h2>${lesson.title}</h2>
<p>${lesson.description}</p>
`;

card.onclick=()=>{
openLesson(index);
};

grid.appendChild(card);
});
}

function openLesson(index){
currentLesson=index;

const lesson=lessons[currentTopic].items[index];
const data=lessons[currentTopic];

document.getElementById("lesson-category").textContent=data.label;
document.getElementById("lesson-title").textContent=lesson.title;
document.getElementById("lesson-intro").textContent=lesson.intro;
document.getElementById("lesson-explanation").textContent=lesson.explanation;
document.getElementById("lesson-code").value = lesson.code;
document.getElementById("lesson-output").textContent="Run the example to see the output.";
document.getElementById("lesson-key").textContent=lesson.key;

document.getElementById("animation-area").innerHTML="";
updateNextButton();

document.getElementById("home-view").classList.add("hidden");
document.getElementById("topic-view").classList.add("hidden");
document.getElementById("lesson-view").classList.remove("hidden");

window.scrollTo(0,0);
}

function backToTopic(){
openTopic(currentTopic);
}

function runExample(){
    if(window.runPythonCode){
        window.runPythonCode();
    }else{
        document.getElementById("lesson-output").textContent =
            "Python is still loading. Please try again.";
    }
}

function updateNextButton(){
const items=lessons[currentTopic].items;
const button=document.getElementById("next-button");
const title=document.getElementById("next-title");

if(currentLesson<items.length-1){
title.textContent=items[currentLesson+1].title;
button.disabled=false;
button.style.opacity="1";
}else{
title.textContent="Topic complete!";
button.disabled=true;
button.style.opacity=".5";
}
}

function nextLesson(){
const items=lessons[currentTopic].items;

if(currentLesson<items.length-1){
openLesson(currentLesson+1);
}
}

function startPythonAnimation(){
if(window.pythonAnimate){
window.pythonAnimate(currentTopic,lessons[currentTopic].items[currentLesson].title);
}else{
document.getElementById("animation-area").innerHTML="<p>Loading Python animation...</p>";
}
}

showHome();