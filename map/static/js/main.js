var LeafIcon = L.Icon.extend({
    options: {
        shadowUrl: '',
        iconSize: [40, 40],
        shadowSize: [50, 64],
        iconAnchor: [20, 0],
        shadowAnchor: [4, 62],
        popupAnchor: [0, 0]
    }
});


window.addEventListener("map:init", function (event) {
    var map = event.detail.map;
    map.addControl(new L.Control.Fullscreen({ position: 'bottomleft' }));

    var userlatlng = 0;

    function onLocationFound(e) {

        var radius = e.accuracy / 2;
        userlatlng = e.latlng;
        current_accuracy = L.circle(e.latlng, radius);
        current_position = L.marker(e.latlng);
        current_position.addTo(map).bindPopup("You are here");
        current_accuracy.addTo(map);
    }

    function onLocationError(e) {
        alert(e.message);
    }

    map.on('locationfound', onLocationFound);
    map.on('locationerror', onLocationError);

    function locateUser() {
        map.removeLayer(current_position);
        map.removeLayer(current_accuracy);
        map.locate({ setView: true, maxZoom: 15 });
    }

    map.locate({ setView: false });

    window.userPlace = userlatlng.toString().slice(7, -1).split(', ');

    var toLocate = L.easyButton(`<img class="locate" src="${locateImagePath}">`, function (btn, map) {
        locateUser();

        route.getPlan().setWaypoints([userlatlng, center]);
        route.route();
    });

    fetch(`${profileUrl}?quest=${quest}`).then(function (resp) { return resp.json(); })
        .then(function (data) {
            window.profile_data = data;
            if (level <= 1) {
                document.getElementById('profileButton').click();
            }
            else {}
        });

    var profileButton = L.easyButton(`<img class="profileButtonImage" src="${profileImagePath}">`, function (btn, map) {
        var links = ''
        for (i = 1; i <= quests_count; i++) {
            links += `<li class='${profile_data.progress[i].status[2]}'>
          <a href="${questListUrl}${profile_data.progress[i].this_id}/">${profile_data.progress[i].title}</a>:
          ${profile_data.progress[i].progress}
          ${profile_data.progress[i].status[1]}</li>`
        }
        links += '</ul>'
        var content = `
          <br>
          <button id="closeButton">close</button>
          <br>
          <h3>${ profile_data.username } (${ profile_data.full_name })</h3>
          <h2>Quest: ${profile_data.title}</h2>
          <h3>LEVEL: ${profile_data.level} ${profile_data.this_progress}</h3>`
        if (level <= 1) {
            content += `<h3>Hello! You need to buy this quest ;)
          You can do this by click on your first search area and follow instructions.
          Good luck!</h3>
          <p>Tip: to FULLSCREEN the map click on left bottom button after you close this window.</p>`;
        }
        else {}
        content += `<ul><h4>YOUR TOTAL PROGRESS:</h4>`;
        content += links;
        content += `<a href="${logoutUrl}"><button id="logoutButton">Logout</button></a>`;


        sidebar.show();
        sidebar.setContent(content);
        document.getElementById("closeButton").onclick = hideSidebar
    }, { id: 'profileButton', position: 'bottomright' });

    map.addControl(profileButton);

    var buttons = [];
    buttons.push(toLocate);

    var sidebar = L.control.sidebar('sidebar', {
        closebutton: true,
        position: 'right'
    });

    map.addControl(sidebar);

    function hideSidebar() {
        sidebar.hide();
    }

    window.count = 0;

    function contentPolygons(data) {
        var color = "";

        L.geoJson(data, {
            onEachFeature: function onEachFeature(feature, layer) {
                var content = `
            <button id="closeButton">close</button>
            <br><br><img width="100" height="50" src="${feature.properties.picture}"/>
            <h3 id="title">${feature.properties.title}</h3>
            <p>${feature.properties.description}</p>
            <br>
            <button id="walkingButton">Walking directions</button>
            <button id="drivingButton">Driving directions</button>
            <button id="cyclingButton">Cycling directions</button>
            <button id="hideRouterButton">Hide directions</button>
            <button id="directionsButton">Google Maps directions</button>
            <br>
            <ul id = "directionsList">`;

                function sidebarButtons() {
                    document.getElementById('closeButton').onclick = hideSidebar;
                    document.getElementById('directionsButton').onclick = directionsButton;
                    document.getElementById('hideRouterButton').onclick = function () {
                        sidebar.hide();
                        map.removeControl(route);
                        count = 0;
                    };

                    document.getElementById('walkingButton').onclick = function () {
                        sidebar.hide();

                        route.getRouter().options.profile = 'mapbox/walking';
                        route.getPlan().setWaypoints([userlatlng, center]);
                        if (count < 1) {
                            window.route.addTo(map);
                            count += 1;
                        }
                        else {
                            route.route();
                        }
                    }

                    document.getElementById('drivingButton').onclick = function () {
                        sidebar.hide();

                        route.getRouter().options.profile = 'mapbox/driving';
                        route.getPlan().setWaypoints([userlatlng, center]);
                        if (count < 1) {
                            window.route.addTo(map);
                            count += 1;
                        }
                        else {
                            route.route();
                        }
                    }

                    document.getElementById('cyclingButton').onclick = function () {
                        sidebar.hide();

                        route.getRouter().options.profile = 'mapbox/cycling';
                        route.getPlan().setWaypoints([userlatlng, center]);
                        if (count < 1) {
                            window.route.addTo(map);
                            count += 1;
                        }
                        else {
                            route.route();
                        }
                    }
                }


                window.route = L.Routing.control({
                    waypoints: [userlatlng, center],
                    fitSelectedRoutes: false,
                    createMarker: function () { return null; },
                    router: L.Routing.mapbox('pk.eyJ1IjoiaW1ndm9pZCIsImEiOiJjam9rb2pjdTUwYzNoM3Zub3RqajNjd21qIn0.p3FJ-deF-vck6YdoScgFIA', { profile: false }),
                    routeLine: function (route) {
                        var line = L.Routing.line(route, {
                            addWaypoints: false,
                            extendToWaypoints: false,
                            routeWhileDragging: false,
                            autoRoute: true,
                            useZoomParameter: false,
                            draggableWaypoints: false,
                            fitSelectedRoutes: false
                        });
                        line.eachLayer(function (l) {
                            l.on('click', function (e) {
                                sidebar.show();
                                sidebar.setContent(content);
                                sidebarButtons();
                            });
                        });
                        return line;

                    }
                });

                var directionsButton = function () {
                    userPlace = userlatlng.toString().slice(7, -1).split(', ');
                    directions = `https://www.google.com/maps/dir/?api=1&origin=${center[0]},${center[1]}&destination=${userPlace[0]},${userPlace[1]}&travelmode=`
                    contentDirections = `
              <li><a class = "directionsLink" href="${directions}walking" target="_blank">Walking</a></li>
              <li><a class = "directionsLink" href="${directions}driving" target="_blank">Driving</a></li>
              <li><a class = "directionsLink" href="${directions}transit" target="_blank">City Transport</a></li>`
                    document.getElementById("directionsList").innerHTML = contentDirections;
                }


                layer.on('click', function () {
                    sidebar.show();
                    sidebar.setContent(content);
                    sidebarButtons();
                });


                color = feature.properties.color;
            },
            style: function (feature) {
                return { "color": feature.properties.color }
            }
        }).addTo(map);
    }

    function contentMarkers(data) {
        L.geoJson(data, {
            onEachFeature: function onEachFeature(feature, layer) {
                var content = `<button id="closeButton">close</button><br><br><img width="100" height="50" src="${feature.properties.picture_url}"/><h3>${feature.properties.title}</h3><p>${feature.properties.description}</p>`;
                layer.on('click', function () {
                    sidebar.show();
                    sidebar.setContent(content);
                    document.getElementById("closeButton").onclick = hideSidebar;
                });
            },
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, { icon: new LeafIcon({ iconUrl: feature.properties.icon }) });
            }
        }).addTo(map);
    }

    contentMarkers(marker);
    contentPolygons(polygon);

    toPolygon = L.easyButton(
        `<img class="locate" src="${toQuestImagePath}">`,
        function (btn, map) {
            map.flyTo(center);
        }, { id: 'toPolygonButton' });

    buttons.push(toPolygon);
    L.easyBar(buttons).addTo(map);

});
