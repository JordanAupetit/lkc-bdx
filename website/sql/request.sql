-- - Ajout d'un Tuple 
-- - Modification d'un Tuple 
-- - Suppression d'un type 
-- - Suppression d'un matériel, tag, option 
-- - Recherche d'un tuple via le nom de l'option du tag ou du matériel

-- recherche de la liste des options pour un marériel donné
SELECT `option`.`id` AS `id`, `option`.`name` AS `name`, 
       `kernel_version`, `kernel_sub`
FROM `option` JOIN `hardware_option` ON (`option_id` = `option`.`id`)
     	      JOIN `hardware` ON (`hardware_id` = `hardware`.`id`)
WHERE `hardware`.`name` LIKE '%nom_du_materiel%'

-- recherche de la liste des matériels pour une option donnée
SELECT `hardware`.`id` AS `id`, `hardware`.`name` AS `name`, 
       `kernel_version`, `kernel_sub`
FROM `option` JOIN `hardware_option` ON (`option_id` = `option`.`id`)
     	      JOIN `hardware` ON (`hardware_id` = `hardware`.`id`)
WHERE `option`.`name` LIKE '%nom_de_l_option%'

-- ajout d'un tuple materiel - option
-- on verifie que le materiel et / ou l'option n'existent pas déjà
-- si on a des résultats, il faut voir si l'un des membres du tuple que
--    l'utilisateur cherche à ajouter n'est pas dans la liste retournée
--    si oui, il faudra mofifier la chaine entrée par l'utilisateur par 
--    celle qu'il veut dans la liste
SELECT * FROM `hardware` WHERE `name` LIKE '%nom_du_materiel%' ORDER BY `name`
SELECT * FROM `option` WHERE `name` LIKE '%nom_de_l_option%' ORDER BY `name`

-- sinon, on ajoute
INSERT INTO `hardware` (`name`) VALUES ('nom_du_materiel')
INSERT INTO `option` (`name`) VALUES ('nom_de_l_option')

-- et si on garde les id en auto increment / les tables hardware - option
-- il faut récupérer l'id qu'on a pas explicitement dans l'insertion d'avant,
-- pour ensuite faire l'insertion dans la table hardware_option
SELECT `id` AS `hardware_id` FROM `hardware` WHERE `name` = 'nom_du_materiel'
SELECT `id` AS `option_id` FROM `option` WHERE `name` = 'nom_de_l_option'

INSERT INTO `hardware_option` (`hardware_id`, `option_id`) 
       VALUES (id_du_materiel, id_de_l_option)

-- modifier / supprimer un materiel
UPDATE `hardware` SET `name`='nouveau_nom_materiel' WHERE `id` = id_du_materiel
DELETE FROM `hardware_option` WHERE `id` = id_du_materiel
DELETE FROM `hardware` WHERE `id` = id_du_materiel

-- modifier / supprimer une option
UPDATE `option` SET `name`='nouveau_nom_option' WHERE `id` = id_de_l_option
DELETE FROM `hardware_option` WHERE `id` = id_de_l_option
DELETE FROM `option` WHERE `id` = id_de_l_option

-- modifier un tuple en fonction du materiel
