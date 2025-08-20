from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_discount_percent(self):
        discount = self.cleaned_data['discount_percent']
        if discount < 0 or discount > 100:
            raise forms.ValidationError("Discount must be between 0 and 100.")
        return discount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        color = cleaned_data.get("color")
        gender = cleaned_data.get("gender")
        errors = {}

        if category:
            category_name = category.name.lower()

            if "perfume" in category_name:
                if color:
                    errors["color"] = "Perfumes should not have color."
                if gender:
                    errors["gender"] = "Perfumes should not have gender."

            elif "cloth" in category_name:
                if not color:
                    errors["color"] = "Clothes must have color."
                if not gender:
                    errors["gender"] = "Clothes must have gender."

        if subcategory and category and subcategory.category != category:
            errors["subcategory"] = "SubCategory does not belong to selected Category."

        if errors:
            raise ValidationError(errors)
