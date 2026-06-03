from django.shortcuts import render


def landing_choice(request):
    """Root reviewer path chooser between the cake site and BakeOps analytics."""
    return render(request, "landing_choice.html")
