# API GEO Redis

### URLs

1. Deberá tener una vista para agregar lugares a los grupos de interés.<br/>
   http://localhost:5000/add_place?team=Supermercados&latitude=-32.4883138&longitude=-58.2466499&name=Rey

2. Deberá mostrar los lugares de cada grupo que estén dentro de un radio de 5 km, de la
   ubicación del usuario (ingresado por el cliente de forma manual).<br/>
   http://localhost:5000/places?team=Cervecerias&latitude=-32.4835896&longitude=-58.2328188<br/>

3. Deberá devolver la distancia entre la ubicación del usuario y uno de los puntos elegido
   por el usuario de los mostrados en el punto anterior.<br/>
   http://localhost:5000/distance?team=Cervecerias&name=Lagash&latitude=-32.4835896&longitude=-58.2328188
