Stat.getJSON = (event_name, start, end, fields, callback) ->
  url = Stat.queryUrl
  query = JSON.stringify({
    event_name: event_name
    from_datetime: start
    to_datetime: end
  })
  fields = JSON.stringify fields

  data = {
    app_name: Stat.appName
    query: query
    fields: fields
  }
  $.getJSON url, data, (data) ->
    callback data


Stat.getCreateClipStat = (start, end, fields, callback) ->
  Stat.getJSON 'create_clip', start, end, fields, callback


Stat.visualization = (data, type, title, node) ->
  options = title: title
  charts =
    LineChart: (node) -> new google.visualization.LineChart(node)
    PieChart: (node) -> new google.visualization.PieChart(node)
    BarChart: (node) -> new google.visualization.BarChart(node)
    ColumnChart: (node) -> new google.visualization.ColumnChart(node)

  chart = charts[type](node)
  chart.draw(data, options)

