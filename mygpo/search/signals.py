
def remove_podcast_entry(sender, instance=False, **kwargs):
    from mygpo.search.models import SearchEntry
    SearchEntry.objects.filter(obj_type='podcast', obj_id=instance.id).delete()

def remove_podcast_group_entry(sender, instance=False, **kwargs):
    from mygpo.search.models import SearchEntry
    SearchEntry.objects.filter(obj_type='podcast_group', obj_id=instance.id).delete()

def update_podcast_entry(sender, instance=False, **kwargs):
    from mygpo.search.models import SearchEntry
    # we don't want podcasts in groups to be indexed separately
    if instance and not instance.group:
        SearchEntry.objects.filter(obj_type='podcast', obj_id=instance.id).delete()
        entry = SearchEntry.from_object(instance)
        entry.save()

def update_podcast_group_entry(sender, instance=False, **kwargs):
    from mygpo.search.models import SearchEntry

    for podcast in instance.podcasts():
        SearchEntry.objects.filter(obj_type='podcast', obj_id=podcast.id).delete()

    SearchEntry.objects.filter(obj_type='podcast_group', obj_id=instance.id).delete()
    entry = SearchEntry.from_object(instance)
    entry.save()

