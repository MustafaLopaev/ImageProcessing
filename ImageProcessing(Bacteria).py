from PIL import Image
from scipy import misc
import numpy as np
from random import sample, randint
import math

def logical_xor(str1, str2):
    return str1 ^ str2


def crop(image_path, coords, saved_location):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)


def swap(sequence, i, j):
    temp = sequence[i]  # Düğüm yer değiştirme fonksiyonu
    sequence[i] = sequence[j]
    sequence[j] = temp


def calculateDistance(path):
    index = path[0]  # Düğümler arası uzaklık hesabı
    distance = 0
    for nextIndex in path[1:]:
        distance += distanceMatrix[index][nextIndex]
        index = nextIndex
    return distance;


def elimination(bacteria, a, b, c, d):
    bacteria = bacteria[0][:]  # Elimisanyon süreci
    swap(bacteria, a, b)
    swap(bacteria, b, c)
    swap(bacteria, c, d)
    swap(bacteria, a, d)
    return (bacteria, calculateDistance(bacteria))


def kemotaxis(bacteria, a, b):
    bacteria = bacteria[0][:]  # Kemotaksis süreci
    swap(bacteria, a, b)
    return (bacteria, calculateDistance(bacteria))


def bacteria(num1, distanceMatrix):
    numBacteria = num1  # Bakteri sayısı
    worstBacteria = int(0.5 * numBacteria)  # Değersiz bakteriler

    maxGen = 20  # Bakteri jenerasyon sayısı

    n = len(distanceMatrix)  # Düğümlerin sayısı

    bacteria = []  # Bakteriler için array

    initPath = list(range(0, n))  # Rota
    index = 0

    for i in range(numBacteria):
        rota = sample(initPath, n)
        bacteria.append(
            (rota, calculateDistance(rota)))  # Bakteri sayısı kadar rastgele rota oluşturup yuvalara atanması işlemi

    bacteria.sort(key=lambda x: x[1])  # Bakterilerin maliyete göre sıralanması

    for i in range(maxGen):
        bestBacterium = bacteria[0]  # Düşük maliyetli bakteriyi göç için seç

        for j in range(n):
            copyBestBacterium = kemotaxis(bestBacterium, randint(0, n - 1), randint(0, n - 1))  # kemotaksis

            if (bacteria[j][1] > copyBestBacterium[
                1]):  # Bir sonraki bakteri maliyeti daha yüksekse bakterileri değiştir.
                bacteria[j] = copyBestBacterium
        bacteria.sort(key=lambda x: x[1])

        for kk in range(numBacteria - worstBacteria, numBacteria):  # Kötü değerli bakterileriler yeniden işleniyor
            bacteria[kk] = kemotaxis(bacteria[kk], randint(0, n - 1), randint(0, n - 1))  # Üreme
        bacteria.sort(key=lambda x: x[1])

        if (randint(0, 10000) == 0):
            for j in range(n):  # Eliminasyon işlemi  %0.01 ihtimalle
                bacteria[j] = elimination(bestBacterium, randint(0, n - 1), randint(0, n - 1), randint(0, n - 1),
                                          randint(0, n - 1))
            bacteria.sort(key=lambda x: x[1])

    return bacteria[0][0]


if __name__ == '__main__':
    image = 'Photos2.jpg'
    filename = Image.open(image)
    im1 = Image.open('Photos2.jpg')
    rgb_im1 = im1.convert('RGB')
    t = math.ceil(filename.size[0] / 5)
    t1 = math.ceil(filename.size[1] / 5)
    k = math.ceil(filename.size[0])
    k1 = math.ceil(filename.size[1])
    im2 = Image.new('RGB', (k, k1))

    list1 = []
    list1c = list(range(26))
    list2 = list(range(t * t1 * 3))
    list3 = list(range(25))
    s1, s2, s3, s4, s5 = [0, 0, 0, 0, 0]
    s6 = 1

    size = filename.size[0] / 5
    tt = filename.size[0] / 5
    size1 = filename.size[1] / 5
    tt1 = filename.size[1] / 5
    kk = 0
    kk1 = 0
    s = 0
    q = list(range(25))
    for i in range(0, 5):
        for j in range(0, 5):
            crop(image, (kk, kk1, size, size1), 'cropped.jpg')
            image1 = misc.imread('cropped.jpg', mode="L")
            hist, bin_edges = np.histogram(image1, bins='auto')
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            im_min = image1.min()
            im_max = image1.max()
            im_mean = image1.mean()
            q[s] = im_mean
            s = s + 1
            kk1 = kk1 + tt1
            size1 = size1 + tt1
        kk = kk + tt
        kk1 = 0
        size1 = tt1
        size = size + tt
    s1 = 0

    distanceMatrix = list()
    for i in range(0, 25):
        temp = list()
        for j in range(0, 25):
            temp.append(abs(q[i] - q[j]))
        distanceMatrix.append(temp)

    list1 = bacteria(25, distanceMatrix)

    for i in range(25):
        list1[i] = list1[i] + 1
        list1c[i] = list1[i]

    for l in range(0, 25):
        for l1 in range(0, 5):
            if list1c[l] > 5:
                list1c[l] = list1c[l] - 5
                s2 = s2 + 1
            else:
                break
        if s6 == 1:
            for i in range((list1c[l] - 1) * t, t * list1c[l]):
                for j in range(s2 * t1, (s2 + 1) * t1):
                    r, g, b = rgb_im1.getpixel((i, j))
                    list2[s1] = r
                    list2[s1 + 1] = g
                    list2[s1 + 2] = b
                    im2.putpixel((i, j), (list2[s1], list2[s1 + 1], list2[s1 + 2]))
                    s1 = s1 + 3
        else:
            for i in range((list1c[l] - 1) * t, t * list1c[l]):
                for j in range(s2 * t1, (s2 + 1) * t1):
                    r, g, b = rgb_im1.getpixel((i, j))
                    list2[s1] = logical_xor(list2[s1], r)
                    list2[s1 + 1] = logical_xor(list2[s1 + 1], g)
                    list2[s1 + 2] = logical_xor(list2[s1 + 2], b)

                    im2.putpixel((i, j), (list2[s1], list2[s1 + 1], list2[s1 + 2]))
                    s1 = s1 + 3
        s1 = 0
        s6 = s6 + 1
        s2 = 0
    im2.save('pixel.jpg')
    Photo1 = 'pixel.jpg'
    filename2 = Image.open(Photo1)
    filename2.show()
