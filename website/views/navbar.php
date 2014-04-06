<?php 
    // Reporte toutes les erreurs PHP
    error_reporting(E_ALL);
    ini_set('display_errors', -1);
?>

<nav class="navbar navbar-inverse" role="navigation">
    <div class="navbar-header">
        <a class="navbar-brand" href="#">Linux Kernel Configuration</a>
    </div>
    <div class="container-fluid">
        <div class="collapse navbar-collapse">
            <a style="text-decoration:none;" href="page_hardware.php">
                <button class="btn btn-primary navbar-btn">Hardware / Options</button>
            </a>
            <a style="text-decoration:none;" href="page_tag.php">
                <button class="btn btn-primary navbar-btn">Tags / Options</button>
            </a>
            <a style="text-decoration:none;" href="#">
                <button class="btn btn-info navbar-btn btn-help">Help</button>
            </a>
        </div>
    </div>
</nav>


<div class="modal fade" id="modalHelp" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">Help</h4>
            </div>
            <div class="modal-body">
                This site was made to create a community database for the 
                application "Linux Kernel Configuration". <br>
                Indeed, it is possible to create relationships 
                between equipment and options but also between tags and options. <br>
                Later these data can be used in the application to facilitate its use.
            </div>
        </div>
    </div>
</div>