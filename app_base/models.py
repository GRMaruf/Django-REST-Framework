from django.db import models

# for validations
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image

# for image compression
from io import BytesIO
from django.core.files import File


#  validators
def validate_file_size(file):
    if file.size > 0.25 * 1024 * 1024: # 1024 * 1024 = 1MB
        raise ValidationError("Max file size is 206KB.")

def validate_image_type(file):
    try:
        img = Image.open(file)
        if img.format not in ['JPEG', 'PNG']:
            raise ValidationError("Only JPEG and PNG are allowed.")
    except Exception:
        raise ValidationError("Invalid image file.")

def validate_image_resulation(image):
    img = Image.open(image)
    width, height = img.size

    if width < 100 or height < 100:
        raise ValidationError(f"Minimum resolution is 100x100 px, but given {width}x{height}.")

    if width > 300 or height > 300:
        raise ValidationError(f"Maximum resolution is 300x300 px, but given {width}x{height}.")

def title_validate(value):
    if not 4 < len(value) < 201:
        raise ValidationError("Title must be between 5 to 200 characters.")
    
def price_validate(value):
    if value < 0:
        raise ValidationError("Price cannot be negative.")
    elif value == 0:
        raise ValidationError("Price cannot be Zero.")
    
def quantity_validate(value):
    if value < 0:
        raise ValidationError("Quantity cannot be negative.")
    elif value == 0:
        raise ValidationError("Quantity cannot be Zero.")

# Models
class ProductInfo(models.Model):
    product_id = models.CharField('Product ID', max_length=50, default="username_ID")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(
        default=0.0,
        validators=[price_validate]
    )
    quantity = models.FloatField(
        default=0,
        validators=[quantity_validate]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:50]
    

class ProductImage(models.Model):
    # Use extra input field for multiple image input
    # <input type="file" name="images" multiple>
    product = models.ForeignKey(
        ProductInfo,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products',
        validators=[
            validate_file_size,
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_image_type,
            validate_image_resulation
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            # Convert if PNG with transparency issues
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # image resizing before compression
            # max_size = (1200, 1200)
            # img.thumbnail(max_size)

            output = BytesIO()

            img.save(
                output,
                format='JPEG',
                quality=75,
                optimize=True
            )

            # Compression levels -

            #     95 → very high quality, large file
            #     80 → balanced
            #     70 → good for web
            #     50 → noticeable quality loss

            output.seek(0)

            self.image = File(output, name=self.image.name)

            print(f'\nImage compressed - TRUE\nCompressed size - {round(self.image.size/1024, 2)}KB')
        super().save(*args, **kwargs)