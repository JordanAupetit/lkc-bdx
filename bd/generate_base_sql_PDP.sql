-- phpMyAdmin SQL Dump
-- version 3.1.2deb1ubuntu0.2
-- http://www.phpmyadmin.net
--
-- Serveur: localhost
-- Généré le : Ven 21 Mars 2014 à 15:44
-- Version du serveur: 5.0.75
-- Version de PHP: 5.2.6-3ubuntu4.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Base de données: `jaupetit`
--

-- --------------------------------------------------------

--
-- Structure de la table `hardware`
--

CREATE TABLE IF NOT EXISTS `hardware` (
  `id` int(11) NOT NULL auto_increment,
  `name` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `hardware`
--


-- --------------------------------------------------------

--
-- Structure de la table `hardware_option`
--

CREATE TABLE IF NOT EXISTS `hardware_option` (
  `hardware_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY  (`hardware_id`,`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `hardware_option`
--


-- --------------------------------------------------------

--
-- Structure de la table `option`
--

CREATE TABLE IF NOT EXISTS `option` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `kernel_version` varchar(30) NOT NULL,
  `kernel_sub` varchar(30) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `option`
--


-- --------------------------------------------------------

--
-- Structure de la table `tag`
--

CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL auto_increment,
  `name` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `tag`
--


-- --------------------------------------------------------

--
-- Structure de la table `tag_option`
--

CREATE TABLE IF NOT EXISTS `tag_option` (
  `tag_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY  (`tag_id`,`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `tag_option`
--

