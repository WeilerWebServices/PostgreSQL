var repodata = {{json|safe}};
var supported_versions = [{{supported_versions}}];

function sortNumeric(a,b) {
   return a-b;
}

function get_platform_name(plat) {
    if (plat == 'EL')
	return "RedHat Enterprise, CentOS, Scientific or Oracle";
    else if (plat == 'F')
	return "Fedora";
    return "Undefined distribution";
}

function get_rpm_prefix(plat) {
   if (plat.startsWith('EL-'))
       return 'redhat';
    else if (plat.startsWith('F-'))
	return 'fedora';
    return 'unknown';
}

function get_installer(plat) {
    if (plat.startsWith('F-'))
	return 'dnf';
    else if (plat.startsWith('EL-')) {
	var a = plat.split('-');
	if (a[1] >= 8)
	    return 'dnf';
    }
    return 'yum';
}

function disable_module_on(plat) {
    if (plat.startsWith('EL-')) {
	var a = plat.split('-');
	if (a[1] >= 8)
	    return true;
    }
    return false;
}

function uses_systemd(plat) {
    if (plat.startsWith('EL-')) {
	var a = plat.split('-');
	if (a[1] < 7)
	    return false;
    }
    return true;
}

function get_platform_text(p) {
    var a = p.split('-');
    return get_platform_name(a[0]) + ' version ' + a[1];
}

window.onload = function() {
   for (var p in supported_versions) {
      var opt = document.createElement('option');
      opt.text = supported_versions[p];
      document.getElementById('version').add(opt);
   }

   loadPlatforms();
   archChanged();
}

function verChanged() {
    /* Just update like the architecture changed */
    archChanged();
}

function loadPlatforms() {
   var platbox = document.getElementById('platform');

   while (platbox.options.length > 0) {
      platbox.options.remove(0);
   }
   var opt = document.createElement('option');
   opt.text = '* Select your platform';
   opt.value = -1;
   platbox.add(opt);

   platkeys = Object.keys(repodata['platforms']).sort();
   for (var pp in platkeys) {
      var opt = document.createElement('option');
      opt.text = get_platform_text(platkeys[pp]);
      opt.value = platkeys[pp];
      platbox.add(opt);
   }

   platChanged();
}

function platChanged() {
   var plat = document.getElementById('platform').value;
   var archbox = document.getElementById('arch');

   while (archbox.options.length > 0) {
      archbox.options.remove(0);
   }

   if (plat == -1) {
      archChanged();
      return;
   }

   for (a in repodata['platforms'][plat].sort().reverse()) {
      var opt = document.createElement('option');
      opt.text = opt.value = repodata['platforms'][plat][a];
      archbox.add(opt);
   }

   archChanged();
}

function archChanged() {
   var ver = document.getElementById('version').value;
   var plat = document.getElementById('platform').value;
   var arch = document.getElementById('arch').value;

   if (!plat || plat == -1) {
      document.getElementById('reporpm').innerHTML = 'Select version and platform above';
      document.getElementById('clientpackage').innerHTML = 'Select version and platform above';
      document.getElementById('serverpackage').innerHTML = 'Select version and platform above';
      document.getElementById('initdb').innerHTML = 'Select version and platform above';
      document.getElementById('dnfmodule').style.display = 'none';
      return;
   }

   var pinfo = repodata['platforms'][plat];
   var shortver = ver.replace('.', '');

   var url = 'https://download.postgresql.org/pub/repos/yum/reporpms/' + plat + '-' + arch + '/pgdg-' + get_rpm_prefix(plat) +'-repo-latest.noarch.rpm';

   var installer = get_installer(plat);
   document.getElementById('reporpm').innerHTML = installer + ' install ' + url;
   document.getElementById('clientpackage').innerHTML = installer + ' install postgresql' + shortver;
   document.getElementById('serverpackage').innerHTML = installer + ' install postgresql' + shortver + '-server';

   document.getElementById('dnfmodule').style.display = disable_module_on(plat) ? 'list-item' : 'none';

   if (uses_systemd(plat)) {
       var setupcmd = 'postgresql-' + shortver + '-setup';
       if (ver < 10) {
	   setupcmd = 'postgresql' + shortver + '-setup';
       }

       document.getElementById('initdb').innerHTML = '/usr/pgsql-' + ver + '/bin/' + setupcmd + ' initdb<br/>systemctl enable postgresql-' + ver + '<br/>systemctl start postgresql-' + ver;
   }
   else {
       document.getElementById('initdb').innerHTML = 'service postgresql-' + ver + ' initdb<br/>chkconfig postgresql-' + ver + ' on<br/>service postgresql-' + ver + ' start';
   }
}
