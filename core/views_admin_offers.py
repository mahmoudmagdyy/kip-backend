from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Offer
from .serializer import OfferSerializer, OfferCreateSerializer, OfferUpdateSerializer


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
                    "image": request.build_absolute_uri(offer.image.url)
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
        
        # Delete old image if exists
        if offer.image:
            offer.image.delete(save=False)
        
        # Save new image
        offer.image = request.FILES['image']
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
    """Create a new offer by uploading only an image (image-only creation)."""
    try:
        if 'image' not in request.FILES:
            return Response({
                'error': 'No image file provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create offer with sensible defaults for required fields
        now = timezone.now()
        offer = Offer(
            title=(request.FILES['image'].name or 'Offer Image'),
            description='',
            discount_type='percentage',
            discount_value=0,
            valid_from=now,
            valid_until=now + timezone.timedelta(days=365),
            status='active',
            is_featured=False,
            created_by=request.user,
        )
        offer.image = request.FILES['image']
        offer.save()

        # Return minimal image-only payload
        image_url = request.build_absolute_uri(offer.image.url) if offer.image else None
        return Response({"image": image_url}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
