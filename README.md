# Demo AWS Nuke

Démonstration de l'utilisation de [AWS Nuke](https://github.com/ekristen/aws-nuke) pour supprimer toutes les ressources
d'un ensemble de comptes AWS dans une OU particulière d'une organization.

> [!IMPORTANT]  
> **Attention** : AWS Nuke est un outil très puissant qui peut supprimer toutes les ressources d'un compte AWS.
> À utiliser avec précaution.

## Principe générale

1. Récupération de la liste des comptes membres de l'OU.
2. Pour chaque compte membre, on assume un rôle spécifique à AWS Nuke qui permet de supprimer les ressources du compte.
3. On lance AWS Nuke pour supprimer les ressources du compte avec les credentials obtenus à l'étape précédente.

## Prérequis de cette démo

- Une organization AWS avec des comptes membres dans une OU particulière.
- Un compte AWS avec les droits nécessaires pour lister les comptes membres de l'OU et pour assumer un role dans ces
  comptes. Il s'agit généralement du rôle `OrganizationAccountAccessRole` dans chaque compte membre.
- Tous les comptes de l'OU doivent avoir un alias associé. Ceci est obligatoire pour AWS nuke.
- Python 3

## Utilisation

```shell
pip install -r requirements.txt
# Export vos credentials AWS pour le compte qui a les droits nécessaires
export PARENT_OU_ID=ou-xxxx-xxxx
export ROLE_NAME=OrganizationAccountAccessRole
python nuke-ou.py
```

## TODO

- Filtrer les ressources à supprimer et/ou garder
- Détecter les ressources non supportées par AWS Nuke
- Désactiver le dry-run


-----------------------------------------Comment j'ai procedé -----

1 - creer une instance ubuntu 

2- installer aws cli

3 -installer aws nuke 

4- Exporter les variable environements

5- Installer python boto3 et les dependances

6-lancer script
