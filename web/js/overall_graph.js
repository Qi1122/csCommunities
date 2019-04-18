var width = $("#chartDiv").width();
var height = $(window).height() * 0.8;

var outerRadius = Math.min(width, height) / 2 - 10,
innerRadius = outerRadius - 24;

var formatPercent = d3.format(".1%");

var arc = d3.arc()
.innerRadius(innerRadius)
.outerRadius(outerRadius);

var layout = d3.chord()
.padAngle(.04)
.sortSubgroups(d3.descending)
.sortChords(d3.ascending);

var path = d3.ribbon()
.radius(innerRadius);

var svg = d3.select("#chartDiv").append("svg")
.attr("width", width)
.attr("height", height)
.append("g")
.attr("id", "circle")
.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

svg.append("circle")
.attr("r", outerRadius);

d3.csv("neighs.csv")
.then(function (neighs) {
d3.json("matrix.json")
.then(function (matrix) {

    // console.log(matrix.length);

    var res = layout(matrix);

    // Compute the chord layout.
    // layout.matrix(matrix);
    // layout(matrix);

    // console.log(matrix[0]);
    // console.log(neighs[0]);

    // Add a group per neighborhood.
    var group = svg
        .datum(res)
        .append("g")
        .selectAll(".group")
        .data(function(d) {return d.groups; })
        .enter().append("g")
        .attr("class", "group")
        .on("mouseover", mouseover);

    // Add a mouseover title.
    group.append("title").text(function (d, i) {
        try {
            // console.log(i);
            // console.log(neighs[i]);
            return neighs[i].name + ": " + formatPercent(d.value) + " of origins";
        }
        catch(e) {
            console.log(e);
        }
    });

    // Add the group arc.
    var groupPath = group.append("path")
        .attr("id", function (d, i) { return "group" + i; })
        .attr("d", arc)
        .style("fill", function (d, i) { return neighs[i].color; });

    // console.log(groupPath);

    // Add a text label.
    var groupText = group.append("text")
        .attr("x", 6)
        .attr("dy", 15);

    groupText.append("textPath")
        .attr("xlink:href", function (d, i) { return "#group" + i; })
        .text(function (d, i) { return neighs[i].name; });

    // Remove the labels that don't fit. :(
    groupText.filter(function (d, i) { return groupPath._groups[0][i].getTotalLength() / 2 - 16 < this.getComputedTextLength(); })
        .remove();

    // Add the chords.
    var chord = svg
        .datum(res)
        .append("g")
        .selectAll(".chord")
        .data(function(d) {return d; })
        // .selectAll(".chord")
        // .data(layout.chords)
        .enter().append("path")
        .attr("class", "chord")
        .style("fill", function (d) { return neighs[d.source.index].color; })
        .attr("d", path);

    // Add an elaborate mouseover title for each chord.
    chord.append("title").text(function (d) {
        return neighs[d.source.index].name
            + " → " + neighs[d.target.index].name
            + ": " + formatPercent(d.source.value)
            + "\n" + neighs[d.target.index].name
            + " → " + neighs[d.source.index].name
            + ": " + formatPercent(d.target.value);
    });

    function mouseover(d, i) {
        chord.classed("fade", function (p) {
            return p.source.index != i
                && p.target.index != i;
        });
    }
});
})
.catch((e) => {
console.log(e);
});