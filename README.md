# pelisalacarta.miequipo
Canal extra para añadir al plugin pelisalacarta, que permite ver los partidos de mi equipo.

#### Ficheros a modificar respecto al pelisalacarta original:

Básicamente hay que modificar la configuración para incorporar un campo de texto con nuestro equipo preferido (settings.conf y settings.xml), el selector de canales principal para añadir un enlace al nuevo canal (channelselector.py) y el launcher.py para importar el código del canal.

.kodi/addons/plugin.video.pelisalacarta/resources/settings.conf  
Añadir la siguiente línea, cambiando Barcelona por tu equipo preferido  
`miequipoprefe=Barcelona`  

.kodi/addons/plugin.video.pelisalacarta/resources/settings.xml  
Añadir la siguiente línea, dentro de `<category label="General">`  
    `<setting id="miequipoprefe" type="text" label="Mi equipo" default="Barcelona"/>`  

.kodi/addons/plugin.video.pelisalacarta/platformcode/xbmc/settings.xml  
Añadir la siguiente línea, después de `<setting id="player_mode" .../>`  
    `<setting id="miequipoprefe" type="text" label="Mi equipo" default="Barcelona"/>`  

.kodi/addons/plugin.video.pelisalacarta/channelselector.py  
Añadir la siguiente línea, dentro de def getmainlist():  
    `itemlist.append( Item(title="Mi equipo" , channel="miequipo" , action="mainlist" ) )`  

.kodi/addons/plugin.video.pelisalacarta/platformcode/xbmc/launcher.py  
Dentro de def run():, detrás de:  
            if channel_name=="buscador":  
                import pelisalacarta.buscador as channel  
Añadir:  
            `elif channel_name=="miequipo":`  
                `import pelisalacarta.miequipo as channel`  


#### Ficheros a añadir respecto al pelisalacarta original:

.kodi/addons/plugin.video.pelisalacarta/pelisalacarta/miequipo.py
Código principal del canal

.kodi/addons/plugin.video.pelisalacarta/serverssports
Código de detección de videos en diferentes servidores


### Notas:

- Para ver deportes en general, utilizo el plugin SportsDevil (DigiTele Sports) que permite acceder a muchos sitios. Pero me interesa un plugin que directamente me muestre los links de mi equipo y a poder ser que sea más rápido que SportsDevil. Seguramente sería mejor retocar SportsDevil para filtrar mi equipo, pero como conozco mejor pelisalacarta lo he metido ahí.

- Para pruebas, abrir web rojadirecta.me o la que sea, buscar algun evento que se esté emitiendo en ese momento, y en la configuración de pelisalacarta poner como equipo preferido el nombre de uno de los equipos que esté jugando.

- web lshunter (drakulastream):
Los enlaces "principales" tipo javascript:openWindow(...) funcionan ok.
Los enlaces "other links" tipo javascript:openwindow(...) o links externos dependen del servidor que utilizen.

- web rojadirecta:
Los enlaces dependen de servidores externos. Para partidos de la liga española, los principales parecen ser: ucaster, ustream, iguide, ezcast, ?

- web firstrowsports (ifeed2all):
Los enlaces dependen de servidores externos.


### Pendiente:

- Maquear un poco (imágenes, ...)
- Incorporar nuevos servidores, empezando por los que más se utilizen. Una vez identificado el servidor, partir del plugin SportsDevil, en resources/catchers, para ver como lo han resuelto ellos y trasladarlo a código python.


### Servidores probados: 

- [x] lshstream : ok
- [ ] ucaster/tashtv : url final teóricamente resuelta, pero el rtmp no se reproduce y deja colgado el Kodi (probado solo en Ubuntu).
- [ ] iguide : teóricamente resuelta url, pero pendiente comprobarlo
- [ ] 04stream : teóricamente resuelta url, pero pendiente comprobarlo
- [ ] liveall : teóricamente resuelta url, pero pendiente comprobarlo
- [ ] ezcast : teóricamente resuelta url, pero pendiente comprobarlo
- [ ] ustream : teóricamente resuelta url, pero pendiente comprobarlo
- [x] tutele : ok
