Stat.WidgetMixin = Ember.Mixin.create
  refresh: (e) ->
    @controller.refresh()

Stat.TrendingView = Ember.View.extend
#  controller is binded during initialization
#  chartType is binded during initialization
  template: '''
    <div {{bindAttr class="view.rendered :chart"}}></div>
  '''
  didInsertElement: ->
    @draw()

  draw: ->
    node = @$('.chart')
    visualization @get('controller').get('content'), @get('chartType'), node[0]

  rendered: (->
    @draw()
    return True
  ).property('controller.content')




