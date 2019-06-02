from sklearn.cluster import KMeans
import PIL.Image

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(color)
    return points

def RGBcolors(imagename):
    img = PIL.Image.open(imagename)
    points = get_points(img)
    Clusters = KMeans(n_clusters=3, random_state=0).fit(points)
    return(Clusters.cluster_centers_)