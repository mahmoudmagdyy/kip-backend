from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import os
import uuid
import time
from .models import Offer
from .serializer import OfferSerializer, OfferCreateSerializer, OfferUpdateSerializer
from .utils import save_media_to_static, get_media_url


@api_view(['GET'])
def admin_offers_list(request):
    """Get all offers for admin dashboard"""
    try:
        # Get query parameters
        search = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        featured = request.GET.get('featured', '')
        sort_by = request.GET.get('sort_by', '-created_at')
        limit = int(request.GET.get('limit', 50))
        offset = int(request.GET.get('offset', 0))
        
        # Build queryset
        offers = Offer.objects.all()
        
        # Apply filters
        if search:
            offers = offers.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        if status_filter:
            offers = offers.filter(status=status_filter)
        
        if featured == 'true':
            offers = offers.filter(is_featured=True)
        elif featured == 'false':
            offers = offers.filter(is_featured=False)
        
        # Apply sorting
        if sort_by in ['title', '-title', 'created_at', '-created_at', 'valid_from', '-valid_from', 'valid_until', '-valid_until']:
            offers = offers.order_by(sort_by)
        else:
            offers = offers.order_by('-created_at')
        
        # Get total count before pagination
        total_count = offers.count()
        
        # Apply pagination
        offers = offers[offset:offset + limit]
        
        # Return image URLs with offer IDs
        image_data = []
        for offer in offers:
            if offer.image:
                image_data.append({
                    "offer_id": offer.id,
                    "image": offer.image  # Image is now a URLField, so it's already a string
                })
            else:
                image_data.append({
                    "offer_id": offer.id,
                    "image": None
                })
        
        return Response(image_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_offers_stats(request):
    """Get offer statistics for admin dashboard"""
    try:
        total_offers = Offer.objects.count()
        active_offers = Offer.objects.filter(status='active').count()
        inactive_offers = Offer.objects.filter(status='inactive').count()
        expired_offers = Offer.objects.filter(status='expired').count()
        featured_offers = Offer.objects.filter(is_featured=True).count()
        
        # Get offers expiring in next 7 days
        seven_days_from_now = timezone.now() + timezone.timedelta(days=7)
        expiring_soon = Offer.objects.filter(
            status='active',
            valid_until__lte=seven_days_from_now,
            valid_until__gte=timezone.now()
        ).count()
        
        return Response({
            'total_offers': total_offers,
            'active_offers': active_offers,
            'inactive_offers': inactive_offers,
            'expired_offers': expired_offers,
            'featured_offers': featured_offers,
            'expiring_soon': expiring_soon
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_offer(request):
    """Create a new offer"""
    try:
        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Set the created_by field to the current user
            offer = serializer.save(created_by=request.user)
            
            # Return the created offer with full details
            response_serializer = OfferSerializer(offer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_offer_detail(request, offer_id):
    """Get a specific offer by ID"""
    try:
        offer = Offer.objects.get(id=offer_id)
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_update_offer(request, offer_id):
    """Update an existing offer"""
    try:
        offer = Offer.objects.get(id=offer_id)
        serializer = OfferUpdateSerializer(offer, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Return the updated offer with full details
            response_serializer = OfferSerializer(offer)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_offer(request, offer_id):
    """Delete an offer"""
    try:
        offer = Offer.objects.get(id=offer_id)
        offer.delete()
        return Response({
            'message': 'Offer deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_toggle_offer_status(request, offer_id):
    """Toggle offer status between active and inactive"""
    try:
        offer = Offer.objects.get(id=offer_id)
        
        if offer.status == 'active':
            offer.status = 'inactive'
        elif offer.status == 'inactive':
            offer.status = 'active'
        else:
            return Response({
                'error': 'Cannot toggle status for expired offers'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        offer.save()
        
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_toggle_offer_featured(request, offer_id):
    """Toggle offer featured status"""
    try:
        offer = Offer.objects.get(id=offer_id)
        offer.is_featured = not offer.is_featured
        offer.save()
        
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_offers_filter_options(request):
    """Get filter options for offers"""
    try:
        # Get unique status values
        status_choices = [choice[0] for choice in Offer.STATUS_CHOICES]
        
        # Get unique discount types
        discount_types = [choice[0] for choice in Offer.DISCOUNT_TYPE_CHOICES]
        
        return Response({
            'status_choices': status_choices,
            'discount_types': discount_types,
            'featured_options': [True, False]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_upload_offer_image(request, offer_id):
    """Upload image for an offer"""
    try:
        offer = Offer.objects.get(id=offer_id)
        
        if 'image' not in request.FILES:
            return Response({
                'error': 'No image file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the uploaded file
        uploaded_file = request.FILES['image']
        
        # Generate unique filename
        file_extension = os.path.splitext(uploaded_file.name)[1]
        timestamp = int(time.time())
        unique_filename = f"offer_{offer_id}_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"
        
        # Save to media directory
        media_dir = settings.MEDIA_ROOT
        os.makedirs(media_dir, exist_ok=True)
        
        # Save file to media directory
        file_path = os.path.join(media_dir, unique_filename)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Update offer with media URL
        offer.image_url = f'/media/{unique_filename}'
        offer.save()
        
        return Response({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_url': f'/media/{unique_filename}',
            'offer_id': offer.id
        }, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_offer_image(request, offer_id):
    """Delete image from an offer"""
    try:
        offer = Offer.objects.get(id=offer_id)
        
        if not offer.image:
            return Response({
                'error': 'No image to delete'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the image file
        offer.image.delete(save=False)
        offer.image = None
        offer.save()
        
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Offer.DoesNotExist:
        return Response({
            'error': 'Offer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_offer_image(request):
    """
    Upload image only — create a minimal Offer with just the image.
    Returns: offer_id and image URL.
    """
    try:
        # Ensure image exists
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES['image']

        # Generate unique filename
        file_extension = os.path.splitext(uploaded_file.name)[1]
        timestamp = int(time.time())
        unique_filename = f"offer_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

        # Check if Cloudinary is enabled
        if os.environ.get('USE_CLOUDINARY', 'False').lower() == 'true':
            # Upload to Cloudinary
            import cloudinary.uploader
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                uploaded_file,
                folder="offers",
                public_id=unique_filename.replace(file_extension, ''),
                resource_type="image"
            )
            
            # Get Cloudinary URL
            image_url = result['secure_url']
            
            # Create minimal Offer instance with Cloudinary URL
            now = timezone.now()
            offer = Offer.objects.create(
                title=uploaded_file.name or "New Offer",
                description="",
                image=image_url,  # Store the full Cloudinary URL
                discount_type="percentage",
                discount_value=0,
                valid_from=now,
                valid_until=now + timezone.timedelta(days=365),
                status="active",
                is_featured=False,
                created_by=request.user
            )
        else:
            # Use image proxy for Render compatibility
            # Save to temp directory
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            file_path = os.path.join(temp_dir, unique_filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Build full image URL using proxy
            image_url = request.build_absolute_uri(f"/api/image-proxy/{unique_filename}")
            
            # Create minimal Offer instance with full proxy URL
            now = timezone.now()
            offer = Offer.objects.create(
                title=uploaded_file.name or "New Offer",
                description="",
                image=image_url,  # Store the full URL directly
                discount_type="percentage",
                discount_value=0,
                valid_from=now,
                valid_until=now + timezone.timedelta(days=365),
                status="active",
                is_featured=False,
                created_by=request.user
            )

        return Response(
            {
                "offer_id": offer.id,
                "image": image_url
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def test_delete_all_offers(request):
    """
    TEST ENDPOINT: Delete all offers (for testing purposes)
    """
    try:
        from .models import Offer
        
        # Delete all offers
        deleted_count = Offer.objects.all().delete()[0]
        
        return Response({
            'success': True,
            'message': f'Deleted {deleted_count} offers',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)