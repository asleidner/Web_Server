import os

def cluster_explore(list_max):
    docstring="""<html>
    <head>
        <title>Cluster Visualization</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <header>
            <h1 class="desktop"><a href="#">transparent</a><b href="#">.ai</b></h1>
            <a id="menu-button" class="mobile" href="#">
               <i class="menu-toggle fas fa-bars"></i>
            </a>
            <h1 class="mobile">CS330: Winter 2021</h1>
         </header>

         <nav>
            <ul>
               <li ><a href="/">Home</a></li>
               <li class="active"><a href="/add-cluster/">New Cluster</a></li>
               <li><a href="#">Browse Clusters</a></li>
               <li><a href="#">Login</a></li>
            </ul>
         </nav>

        <div class="cardoptions">
        <div class="card">
        <subheader>
            <h1 class="desktop">cluster<b>.params </b></h1>
         </subheader>
            <div class="bg-img" style="background-image:url('https://i.ndtvimg.com/i/2015-09/grapes_625x350_61443376353.jpg');"></div>
            <h4 class="card-title">Compare the features of two clusters!</h4>
            <form method="POST" action="{{ url_for('compare_cluster')}}">
                <label for="groups">Cluster A:</label>
                <select name="groups" id="groups">
                    alextoken1
            </select>
            <br><br>
            <label for="groups1">Cluster B:</label>
                <select name="groups1" id="groups1">
                    alextoken1
            </select>
            <br>
            <p><input type="submit" class="submitbtn" value="Submit"></p>
                <br>
            </form>
            

        <div class="hcenter">
        <a href="#" class="btn3">Fake-Evaluate Them!</a>
        </div>
        </div>
        </div>

    </body>
</html>"""



    buttontext=""
    for x in range(1,list_max+1):
        buttontext+=f'<option value="{x}">Cluster {x}</option>'

    docstring = docstring.replace('alextoken1', buttontext)


    if os.path.exists('templates/cluster-explore.html'):
        os.remove('templates/cluster-explore.html')
    with open('templates/cluster-explore.html', 'w') as f:
        f.write(docstring)
        f.close()



def cluster_explore2(list_max,list_diff,list_same,clustera,clusterb):
    docstring = """<html>
    <head>
        <title>Cluster Visualization</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <header>
            <h1 class="desktop"><a href="#">transparent</a><b href="#">.ai</b></h1>
            <a id="menu-button" class="mobile" href="#">
               <i class="menu-toggle fas fa-bars"></i>
            </a>
            <h1 class="mobile">CS330: Winter 2021</h1>
         </header>

         <nav>
            <ul>
               <li ><a href="/">Home</a></li>
               <li class="active"><a href="/add-cluster/">New Cluster</a></li>
               <li><a href="#">Browse Clusters</a></li>
               <li><a href="#">Login</a></li>
            </ul>
         </nav>

        <div class="cardoptions">
        <div class="card3">
        <subheader>
            <h1 class="desktop">cluster<b>.params </b></h1>
         </subheader>
            <div class="bg-img" style="background-image:url('https://i.ndtvimg.com/i/2015-09/grapes_625x350_61443376353.jpg');"></div>
            <h4 class="card-title">Compare the features of two clusters!</h4>
            <form method="POST" action="{{ url_for('compare_cluster2')}}">
                <label for="groups">Cluster A:</label>
                <select name="groups" id="groups">
                    alextoken1
            </select>
            <br><br><br><br>
            <label for="groups1">Cluster B:</label>
                <select name="groups1" id="groups1">
                    alextoken2
            </select>
            <br><br><br>
            <p><input type="submit" class="submitbtn" value="Submit"></p>
                <br>
            </form>
        </div>
        
        <div class="card3">
            <subheader>
            <h1 class="desktop">comparison<b>.results </b></h1>
            </subheader>
            <div class="bg-img" style="background-image:url('https://venngage-wordpress.s3.amazonaws.com/uploads/2018/03/Comparison-Infographic-Templates-and-Data-Visualization-Tips.jpg');"></div>
            <div class="card-block">
                <p class="card-text">
                Based upon a 2 sided t-test and a P value of <0.05: <br><br>
                The features that are different between alextoken3 <br><br>
                The features that are the same between alextoken4
                </p>
                <a href="#" class="btn">Browse</a>
            </div>
            </div>
                    
        </div>
        
        
        <div class="hcenter">   
        <a href="#" class="btn3">Fake-Evaluate Them!</a>
        </div>

    </body>
</html>"""

    buttontext = ""
    for x in range(1, list_max + 1):
        if x==clustera+1:
            buttontext += f'<option value="{x}" selected>Cluster {x}</option>'
        else:
            buttontext += f'<option value="{x}">Cluster {x}</option>'

    buttontext2 = ""
    for x in range(1, list_max + 1):
        if x==clusterb+1:
            buttontext2 += f'<option value="{x}" selected>Cluster {x}</option>'
        else:
            buttontext2 += f'<option value="{x}">Cluster {x}</option>'

    differ_text=f'Cluster {clustera+1} and Cluster {clusterb+1}: '
    same_text=f'Cluster {clustera+1} and Cluster {clusterb+1}: '

    for feature in list_diff:
        differ_text +=f'{feature}, '

    differ_text=differ_text[:-2]
    differ_text+='.'

    for feature in list_same:
        same_text +=f'{feature}, '

    same_text=same_text[:-2]
    same_text += '.'


    docstring = docstring.replace('alextoken1', buttontext)
    docstring = docstring.replace('alextoken2', buttontext2)
    docstring = docstring.replace('alextoken3', differ_text)
    docstring = docstring.replace('alextoken4', same_text)

    if os.path.exists('templates/cluster-explore2.html'):
        os.remove('templates/cluster-explore2.html')
    with open('templates/cluster-explore2.html', 'w') as f:
        f.write(docstring)
        f.close()

