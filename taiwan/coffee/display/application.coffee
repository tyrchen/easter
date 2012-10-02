window.Stat or= Ember.Application.create
  ready: ->
    @_super()
    Stat.queryUrl = 'http://localhost:8000/api/v1/event/'
    Stat.appName = 'cayman'


