from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, View, ListView

from apps.album.models import Album, Event, Photo


class AlbumListView(ListView):

    model = Album


class EventListView(ListView): 

    model = Event


class AlbumDetailView(DetailView):

    queryset = Album.objects.all()


class EventDetailView(DetailView):

    queryset = Event.objects.all()


class EventSlideshowView(EventDetailView):

    template_name = "album/slideshow.html"


class AlbumSlideshowView(AlbumDetailView):

    template_name = "album/slideshow.html"


class PhotoDetailView(View):

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if kwargs['collection_type'] == 'events':
            collection = get_object_or_404(Event, slug=kwargs['collection_slug'])
            collections_url = reverse('event-list')
            collections_name = 'event'
        elif kwargs['collection_type'] == 'albums':
            collection = get_object_or_404(Album, slug=kwargs['collection_slug'])
            collections_url = reverse('album-list')
            collections_name = 'album'
        else:
            collection = None
            collections_url = None
            collections_name = None

        previous_photo = None
        next_photo = None
        photo_position = 0

        if collection:
            photo_position = list(collection.photo_set.all()).index(photo)
            try:
                previous_photo = collection.photo_set.all()[photo_position-1]
            except (IndexError, AssertionError):
                pass

            try:
                next_photo = collection.photo_set.all()[photo_position+1]
            except (IndexError):
                pass

        context = {
            'object' : photo,
            'collection' : collection,
            'collections_url' : collections_url,
            'collections_name' : collections_name,
            'previous_photo' : previous_photo,
            'next_photo' : next_photo,
            'current_photo_number' : photo_position + 1
        }

        if collections_name is not None:
            return render_to_response(
                'album/%s_photo_detail.html' % collections_name, 
                context, 
                context_instance=RequestContext(request)
            )
        else:
            return render_to_response(
                'album/photo_detail.html' % collections_name, 
                context, 
                context_instance=RequestContext(request)
            )