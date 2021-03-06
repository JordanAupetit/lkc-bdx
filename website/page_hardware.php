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
        <?php include 'views/alert.php'; ?>

        <ul class="nav nav-tabs">
            <li class="active"><a href="#home" data-toggle="tab">Add new relationship</a></li>
            <li class="onglet-search-hardware"><a href="#profile" data-toggle="tab">Search an existing relationship</a></li>
        </ul>

        <div class="tab-content">
            <?php include 'views/tab_add_hardware.php' ?>
            <?php include 'views/tab_update_hardware_option.php' ?>
        </div>
    </div>
</body>
</html>