Parfait, tout roule
Alors pour nos modèles, je vais avoir plusieurs exigences
Déjà en terme d'accès utilisateur, je vois plusieurs choses
- Un compte administrateur (built-in django, pas de socui là dessus)
- Un accès "client" qui permet de voir majoritairement les dashboard, des vues d'exploration, et quelques actions
- Un accès "analyste" beaucoup plus précis, et éventuellement avec des capacités à rechercher des objets etc

Un analyste pourrait par exemple voir plusieurs vues client

Pour ça, j'aimerais que tu me créé des modèles de base, qu'on devrait placer soit dans la partie core soit dans une app distincte de la partie EASM (à mon sens), et qui permet de prédéfinir tout ceci, mais surtout de bien le lier avec le built-in django de la classe auth.user

Par exemple, je vois bien un modèle "client" auquel pluseiurs "user" peuvent être rattachés, et pareil piur l'analyste mais il verait plein de client, un "utilsiateur client" n'en n'a qu'un seul
On peut aussi imaginer des abonnements, par client, etc..., je te laisse me faire une proposition de modèle AVANT de me montrer le code 