-- phpMyAdmin SQL Dump
-- version 3.1.2deb1ubuntu0.2
-- http://www.phpmyadmin.net
--
-- Serveur: localhost
-- Généré le : Dim 06 Avril 2014 à 21:12
-- Version du serveur: 5.0.75
-- Version de PHP: 5.2.6-3ubuntu4.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Base de données: `jaupetit`
--

-- --------------------------------------------------------

--
-- Structure de la table `hardware_lkc`
--

CREATE TABLE IF NOT EXISTS `hardware_lkc` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `constructor` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `hardware_lkc`
--


-- --------------------------------------------------------

--
-- Structure de la table `module_hardware`
--

CREATE TABLE IF NOT EXISTS `module_hardware` (
  `module_name` varchar(255) NOT NULL,
  `hardware_id` int(11) NOT NULL,
  PRIMARY KEY  (`module_name`,`hardware_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `module_hardware`
--


-- --------------------------------------------------------

--
-- Structure de la table `module_lkc`
--

CREATE TABLE IF NOT EXISTS `module_lkc` (
  `name` varchar(255) NOT NULL,
  PRIMARY KEY  (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `module_lkc`
--


-- --------------------------------------------------------

--
-- Structure de la table `module_option`
--

CREATE TABLE IF NOT EXISTS `module_option` (
  `module_name` varchar(255) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY  (`module_name`,`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `module_option`
--


-- --------------------------------------------------------

--
-- Structure de la table `option_lkc`
--

CREATE TABLE IF NOT EXISTS `option_lkc` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `first_seen` varchar(30) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `option_lkc`
--


-- --------------------------------------------------------

--
-- Structure de la table `tag_lkc`
--

CREATE TABLE IF NOT EXISTS `tag_lkc` (
  `name` varchar(255) NOT NULL,
  PRIMARY KEY  (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `tag_lkc`
--


-- --------------------------------------------------------

--
-- Structure de la table `tag_option`
--

CREATE TABLE IF NOT EXISTS `tag_option` (
  `tag_name` varchar(255) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY  (`tag_name`,`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `tag_option`
--


