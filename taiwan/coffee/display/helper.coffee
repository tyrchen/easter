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




