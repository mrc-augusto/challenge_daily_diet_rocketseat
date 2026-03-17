from flask import jsonify

def jsonify_meals(queryset):
  return jsonify([meal.to_dict() for meal in queryset])