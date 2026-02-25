from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product

# Images Robe simple (tes visuels)
ROBE_SIMPLE_IMAGES = [
    "/images/robe-simple-marron.png",
    "/images/robe-simple-bleu.png",
    "/images/robe-simple-noire-mini.png",
    "/images/robe-simple-rose-fluide.png",
    "/images/robe-simple-blanche-sans-bretelles.png",
    "/images/robe-simple-rouge-halter.png",
    "/images/robe-simple-creme-col-v.png",
    "/images/robe-simple-bleu-clair-dentelle.png",
    "/images/robe-simple-rose-brode.png",
    "/images/robe-simple-gris-peplum.png",
    "/images/robe-simple-blanche-dentelle.png",
    "/images/robe-simple-blanche-oeillet.png",
    "/images/robe-simple-bordeaux-drape.png",
    "/images/robe-simple-bleu-marine.png",
    "/images/robe-simple-champagne-brode.png",
]

ABAYA_IMAGES = [
    "/images/abaya-noire-deux-pieces.png",
    "/images/abaya-bordeaux-clutch.png",
    "/images/abaya-vert-brode.png",
    "/images/abaya-beige-dore.png",
    "/images/abaya-vert-sauge-brode.png",
    "/images/abaya-noire-broderie-poignets.png",
    "/images/abaya-greige-imprime.png",
    "/images/abaya-beige-passepoil.png",
    "/images/abaya-beige-manches-cape.png",
    "/images/abaya-taupe-deux-pieces.png",
    "/images/abaya-bordeaux-brode.png",
    "/images/abaya-peche-ceinture-brode.png",
    "/images/abaya-vert-olive.png",
    "/images/abaya-marron-volants.png",
]

PRODUCTS_ROBE_SIMPLE = [
    ("Robe simple marron", "Robe marron à col montant, manches longues et jupe à volants superposés. Coupe modeste et élégante.", Decimal("76.00"), 22),
    ("Robe simple bleu nuit", "Robe bleu petrol à manches évasées et volant à la taille. Tissu fluide et finitions soignées.", Decimal("82.00"), 20),
    ("Robe simple noire mini", "Robe noire mi-genou à manches longues, plissés devant et détail aux poignets. Coupe A.", Decimal("65.00"), 25),
    ("Robe simple rose fluide", "Robe rose pâle sans bretelles, bustier structuré et ceinture drapée. Longueur sol.", Decimal("95.00"), 18),
    ("Robe simple blanche sans bretelles", "Robe blanche longue sans bretelles, plissé à la taille. Silhouette fluide et élégante.", Decimal("88.00"), 20),
    ("Robe simple rouge halter", "Robe rouge bordeaux à encolure halter et décolleté cœur. Jupe fluide jusqu'au sol.", Decimal("92.00"), 16),
    ("Robe simple crème col V", "Robe crème à col V et bretelles, bustier gainé et jupe drapée. Longueur sol.", Decimal("90.00"), 19),
    ("Robe simple bleu clair dentelle", "Robe bleu clair mi-mollet à broderie anglaise et bordure dentelle. Style romantique.", Decimal("72.00"), 22),
    ("Robe simple rose brodée", "Robe rose pâle longue à motif floral brodé, bustier gainé. Tissu vaporeux.", Decimal("98.00"), 15),
    ("Robe simple gris peplum", "Robe gris clair mi-mollet à peplum et fente côté. Coupe structurée.", Decimal("78.00"), 20),
    ("Robe simple blanche dentelle", "Robe blanche mi-genou à bustier dentelle et jupe plissée. Style délicat.", Decimal("85.00"), 18),
    ("Robe simple blanche œillet", "Robe blanche à col bateau, manches courtes et broderie œillet. Jupe ample.", Decimal("75.00"), 21),
    ("Robe simple bordeaux drapée", "Robe bordeaux longue à encolure drapée et plissé côté. Silhouette fluide.", Decimal("94.00"), 17),
    ("Robe simple bleu marine", "Robe bleu marine longue à col ras de cou et panneau flottant. Coupe gainante.", Decimal("86.00"), 19),
    ("Robe simple champagne brodée", "Robe champagne longue à broderie et sequins. Bustier structuré, style soirée.", Decimal("120.00"), 12),
]

PRODUCTS_ABAYA = [
    ("Abaya noire deux pièces", "Ensemble noir à effet scintillant, manches papillon et détail dentelle au poignet.", Decimal("89.00"), 25),
    ("Abaya bordeaux à poignets plissés", "Abaya bordeaux ou prune, tissu texturé, manches à poignets plissés. Élégante et sobre.", Decimal("85.00"), 20),
    ("Abaya vert profond brodée", "Abaya vert forêt ouverte sur robe intérieure, broderie feuillage sur buste et devant.", Decimal("95.00"), 18),
    ("Abaya beige motifs dorés", "Abaya beige à motifs brodés dorés sur buste et manches, finition galon central.", Decimal("88.00"), 22),
    ("Abaya vert sauge broderie perles", "Abaya vert sauge à broderie argent et perles vertes sur manches, coupe fluide.", Decimal("92.00"), 15),
    ("Abaya noire broderie aux poignets", "Abaya noire sobre à broderie géométrique marron et beige sur les manches. Coupe fluide et élégante.", Decimal("86.00"), 20),
    ("Abaya grège imprimé", "Abaya gris-beige à motif discret, plis centraux et manches amples. Style moderne et sobre.", Decimal("84.00"), 18),
    ("Abaya beige passepoil noir", "Abaya beige à passepoil noir sur le devant et plis verticaux. Coupe longue et fluide.", Decimal("82.00"), 22),
    ("Abaya beige manches cape", "Abaya beige fluide à manches cape très amples, tissu satiné. Silhouette volumineuse et élégante.", Decimal("85.00"), 18),
    ("Abaya taupe deux pièces", "Ensemble taupe à manches chauve-souris et ourlet asymétrique. Couche fluide sur robe longue.", Decimal("84.00"), 20),
    ("Abaya bordeaux brodée", "Abaya bordeaux à broderie beige sur buste et manches, glands décoratifs. Coupe ample et fluide.", Decimal("92.00"), 16),
    ("Abaya pêche ceinture brodée", "Abaya pêche à bandeau brodé perles et pierres à la taille et aux poignets. Élégante et sobre.", Decimal("90.00"), 18),
    ("Abaya vert olive", "Abaya vert olive sobre, coupe droite et fluide. Style simple et confortable.", Decimal("78.00"), 22),
    ("Abaya marron à volants", "Abaya marron avec cardigan assorti à volants superposés sur manches et corps. Tissu léger et fluide.", Decimal("88.00"), 19),
]

PARFUM_IMAGES = [
    "/images/parfum-kay-ali-vanilla.png",
    "/images/parfum-armani-rouge.png",
    "/images/parfum-armani-peche.png",
    "/images/parfum-el-nabil-royal-gold.png",
    "/images/parfum-el-nabil-amber-yemen.png",
    "/images/parfum-el-nabil-musc-blanc.png",
    "/images/parfum-emporio-armani-power.png",
    "/images/parfum-el-nabil-medania.png",
    "/images/parfum-kayali-vanilla-candy.png",
    "/images/parfum-kayali-rose.png",
    "/images/parfum-guerlain-aqua-allegoria.png",
    "/images/parfum-el-nabil-musc-coco.png",
    "/images/parfum-ysl-black-opium.png",
]

PRODUCTS_PARFUM = [
    ("Kay Ali Vanilla 28", "Parfum vanille luxe, flacon facetté. Kay Ali.", Decimal("125.00"), 15),
    ("Giorgio Armani", "Parfum signature, flacon dégradé noir et rouge. Giorgio Armani.", Decimal("98.00"), 20),
    ("Giorgio Armani Sì", "Parfum pêche et or, flacon rectangulaire. Giorgio Armani.", Decimal("95.00"), 18),
    ("El Nabil Royal Gold", "Parfum luxe or et noir, flacon facetté. El Nabil.", Decimal("89.00"), 10),
    ("El Nabil Amber of Yemen", "Huile parfumée ambre du Yémen, 5 ml. Flacon or et rubis. El Nabil.", Decimal("45.00"), 25),
    ("El Nabil Musc Blanc", "Parfum musc blanc, flacon blanc et or. El Nabil.", Decimal("75.00"), 20),
    ("Emporio Armani Power of You", "Parfum berry et rose gold. Emporio Armani.", Decimal("72.00"), 22),
    ("El Nabil Medania", "Parfum luxe or, flacon cristal. El Nabil.", Decimal("85.00"), 18),
    ("Kayali Vanilla Candy Rock Sugar 42", "Parfum vanille et sucre. Kayali.", Decimal("118.00"), 14),
    ("Kayali", "Parfum rose et vanille. Kayali.", Decimal("115.00"), 16),
    ("Guerlain Aqua Allegoria Perle Houblonne", "Eau fraîche houblon, flacon rose et or. Guerlain Paris.", Decimal("68.00"), 20),
    ("El Nabil Musc Coco", "Huile parfumée musc coco, 5 ml. El Nabil.", Decimal("42.00"), 28),
    ("Yves Saint Laurent Black Opium", "Parfum Black Opium, flacon noir pailleté. Yves Saint Laurent.", Decimal("105.00"), 18),
]

SAC_IMAGES = [
    "/images/sac-dior-beige.png",
    "/images/sac-dior-rose.png",
    "/images/sac-le-tanneur-marron.png",
    "/images/sac-lavande.png",
    "/images/sac-tricot-marron.png",
    "/images/sac-bordeaux.png",
    "/images/sac-tricot-beige.png",
    "/images/sac-vert-menthe.png",
    "/images/sac-rose-poudre.png",
    "/images/sac-noir-tote.png",
    "/images/sac-marron-plisse.png",
    "/images/sac-creme-croissant.png",
    "/images/sac-le-tanneur-marron-poignee.png",
    "/images/sac-le-tanneur-noir.png",
    "/images/sac-marron-flap.png",
    "/images/sac-le-tanneur-camel.png",
]

PRODUCTS_SAC = [
    ("Sac Dior beige matelassé", "Sac à main beige matelassé cannage, charmes D.I.O.R. et plaque CD. Christian Dior.", Decimal("320.00"), 8),
    ("Sac Dior rose matelassé", "Sac à main rose pâle matelassé cannage, charmes D.I.O.R. dorés. Christian Dior.", Decimal("320.00"), 8),
    ("Sac Le Tanneur marron", "Sac hobo marron camel, piqûre blanche, fermeture zip. Le Tanneur.", Decimal("145.00"), 15),
    ("Sac lavande cuir", "Sac à main lavande en cuir grainé, deux anses, finitions dorées. Coupe épurée.", Decimal("98.00"), 18),
    ("Sac tricot marron", "Sac en tricot câble marron, anses courtes. Style décontracté.", Decimal("65.00"), 22),
    ("Sac bordeaux", "Sac bordeaux souple à une anse, cuir grainé et anneau doré. Silhouette hobo.", Decimal("89.00"), 20),
    ("Sac tricot beige", "Sac en tricot câble beige, anses et finitions dorées. Tendance.", Decimal("62.00"), 24),
    ("Sac vert menthe", "Sac vert menthe structuré à plis, anses et couture contrastée. Style moderne.", Decimal("95.00"), 16),
    ("Sac rose poudre", "Sac rose poudre cuir grainé, anses nouées et boucles dorées. Coupe hobo.", Decimal("88.00"), 19),
    ("Sac noir tote", "Sac tote noir à rabat, piqûre blanche et deux anses. Intemporel.", Decimal("120.00"), 14),
    ("Sac marron plissé", "Sac marron structuré à plis et anses, couture contrastée. Logo discret.", Decimal("110.00"), 15),
    ("Sac crème croissant", "Sac forme croissant crème, bretelle réglable argentée et zip. La Seine.", Decimal("85.00"), 18),
    ("Sac Le Tanneur marron poignée", "Sac marron à poignée unique et bridons en T dorés. Le Tanneur Paris.", Decimal("165.00"), 12),
    ("Sac Le Tanneur noir", "Sac noir structuré, bridons en T argentés, bretelle amovible. Le Tanneur 1898.", Decimal("175.00"), 10),
    ("Sac marron à rabat", "Sac marron à rabat en V et fermetures en T dorées. Coupe classique.", Decimal("155.00"), 11),
    ("Sac Le Tanneur camel", "Sac camel à rabat, bridons dorés et piqûre blanche. Le Tanneur Paris.", Decimal("168.00"), 12),
]


class Command(BaseCommand):
    help = "Seed catégories Femme (Robes traditionnelles > Robe simple, Abaya) et produits."

    def handle(self, *args, **options):
        femme, _ = Category.objects.get_or_create(slug="femme", defaults={"name": "Femme", "parent": None})
        Category.objects.filter(slug="homme").delete()

        robes, _ = Category.objects.get_or_create(
            slug="robes-traditionnelles",
            defaults={"name": "Robes", "parent": femme},
        )
        robes.name = "Robes"
        robes.save(update_fields=["name"])
        robe_simple, _ = Category.objects.get_or_create(
            slug="robe-simple",
            defaults={"name": "Robe simple", "parent": robes},
        )
        abaya, _ = Category.objects.get_or_create(
            slug="abaya",
            defaults={"name": "Abaya", "parent": robes},
        )

        for name, slug in [("Muscs", "muscs"), ("Parfums", "parfums"), ("Sacs", "sacs")]:
            Category.objects.get_or_create(slug=slug, defaults={"name": name, "parent": femme})
        parfums = Category.objects.get(slug="parfums")
        sacs = Category.objects.get(slug="sacs")

        # Anciens produits djellaba -> Robe simple
        old_cat = Category.objects.filter(slug="djellaba-femme").first()
        if old_cat:
            Product.objects.filter(category=old_cat).update(category=robe_simple)
            old_cat.delete()
        # Produits encore dans "robes-traditionnelles" -> Robe simple
        Product.objects.filter(category=robes).update(category=robe_simple)

        Product.objects.filter(category__in=[robe_simple, abaya, parfums, sacs]).delete()

        for i, (name, desc, price, stock) in enumerate(PRODUCTS_ROBE_SIMPLE):
            image_url = ROBE_SIMPLE_IMAGES[i % len(ROBE_SIMPLE_IMAGES)]
            Product.objects.create(
                category=robe_simple,
                name=name,
                description=desc,
                image_url=image_url,
                price=price,
                currency="eur",
                stock=stock,
                is_active=True,
            )

        for i, (name, desc, price, stock) in enumerate(PRODUCTS_ABAYA):
            image_url = ABAYA_IMAGES[i % len(ABAYA_IMAGES)]
            Product.objects.create(
                category=abaya,
                name=name,
                description=desc,
                image_url=image_url,
                price=price,
                currency="eur",
                stock=stock,
                is_active=True,
            )

        for i, (name, desc, price, stock) in enumerate(PRODUCTS_PARFUM):
            image_url = PARFUM_IMAGES[i % len(PARFUM_IMAGES)]
            Product.objects.create(
                category=parfums,
                name=name,
                description=desc,
                image_url=image_url,
                price=price,
                currency="eur",
                stock=stock,
                is_active=True,
            )

        for i, (name, desc, price, stock) in enumerate(PRODUCTS_SAC):
            image_url = SAC_IMAGES[i % len(SAC_IMAGES)]
            Product.objects.create(
                category=sacs,
                name=name,
                description=desc,
                image_url=image_url,
                price=price,
                currency="eur",
                stock=stock,
                is_active=True,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Catégories créées: Robes > Robe simple, Abaya, Parfums, Sacs. Produits ajoutés."
            )
        )
