from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['PokemonApi']
collection = db['Pokemons']

pipeline = [
    {"$unwind": "$types"},
    {"$group": {"_id": "$types.type.name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
result = list(collection.aggregate(pipeline))

data = [{'type': doc['_id'], 'count': doc['count']} for doc in result]
data_json = json.dumps(data)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Gráfico de Pokémon por Tipo</title>
    <script src="https://d3js.org/d3.v5.min.js"></script>
    <style>
        .bar {{
            fill: steelblue;
        }}
        .bar-label {{
            fill: black;
            font-family: Arial, sans-serif;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h2>Gráfico de Cantidad de Pokemon por tipos</h2>
    <svg width="800" height="500"></svg>

    <script>
        var data = {data_json};

        var margin = {{top: 20, right: 30, bottom: 40, left: 90}},
            width = 800 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var svg = d3.select("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleBand()
            .domain(data.map(function(d) {{ return d.type; }}))
            .range([0, width])
            .padding(0.1);

        var y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) {{ return d.count; }})])
            .range([height, 0]);

        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        svg.append("g")
            .call(d3.axisLeft(y));

        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) {{ return x(d.type); }})
            .attr("width", x.bandwidth())
            .attr("y", function(d) {{ return y(d.count); }})
            .attr("height", function(d) {{ return height - y(d.count); }});

        svg.selectAll(".bar-label")
            .data(data)
            .enter().append("text")
            .attr("class", "bar-label")
            .attr("x", function(d) {{ return x(d.type) + x.bandwidth() / 2; }})
            .attr("y", function(d) {{ return y(d.count) - 5; }})
            .attr("text-anchor", "middle")
            .text(function(d) {{ return d.count; }});
    </script>
</body>
</html>
"""

# Guardar el código HTML en un archivo
with open("GraficoCantidadTipos.html", "w") as f:
    f.write(html_code)