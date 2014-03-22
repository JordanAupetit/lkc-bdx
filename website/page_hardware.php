<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <title>Linux Kernel Configuration</title>

    <?php include 'views/include.php'; ?>
</head>
<body>
    <?php include 'views/navbar.php' ?>
    <div class="container mt20">
        <h1 style="text-align:center;" class="mb20">Hardware / Option</h1>

        <ul class="nav nav-tabs">
            <li class="active"><a href="#home" data-toggle="tab">Ajout</a></li>
            <li><a href="#profile" data-toggle="tab">Modification / Suppression</a></li>
        </ul>

        <div class="tab-content">
            <?php include 'views/tab_add_hardware.php' ?>
            <?php include 'views/tab_update_options.php' ?>
        </div>
    </div>
</body>
</html>