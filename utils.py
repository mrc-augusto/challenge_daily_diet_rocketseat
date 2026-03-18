from flask import jsonify

# função para transformar querysets em JSON 
def jsonify_meals(queryset):
  return jsonify([meal.to_dict() for meal in queryset])

# função para validar campos obrigatórios
def validate_required_fields(data, required_fields):
  missing = []
  for field in required_fields:
    value = data.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
      missing.append(field)
  return missing