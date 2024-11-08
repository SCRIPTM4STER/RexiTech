from django import forms
from .models_product import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # Removed the 'product' field
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...',
                'style': 'resize: none;',  # Optional: Prevents resizing
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',  # Example class for Bootstrap styling
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Ensure the comment field is empty
        self.fields['comment'].initial = ''


