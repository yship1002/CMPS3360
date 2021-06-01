/**
 * Created by bsumma on 1/26/16.
 */
var button = d3.select("body").append("button");
button.text("Run!");
button.on("click", execute);