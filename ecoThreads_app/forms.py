from django import forms
from .models import Orders, Address, City, Area

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['order_name', 'description', 'image', 'category']

    # Additional fields from the Address model
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select City")
    area = forms.ModelChoiceField(queryset=Area.objects.none(), empty_label="Select Area")
    pin_code = forms.IntegerField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Set labels for address fields
        self.fields['city'].label = 'City'
        self.fields['area'].label = 'Area'
        self.fields['pin_code'].label = 'Pin Code'
        self.fields['latitude'].label = 'Latitude'
        self.fields['longitude'].label = 'Longitude'
        
        # Add JavaScript attributes for dynamic area selection
        self.fields['city'].widget.attrs['onchange'] = 'update_areas()'
        self.fields['latitude'].widget.attrs.update({'id': 'id_latitude'})
        self.fields['longitude'].widget.attrs.update({'id': 'id_longitude'})

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                print(ValueError)
                pass
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.address.area.city.area_set.order_by('name')

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']