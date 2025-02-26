
async function loadMap() {
    const response =  await fetch('http://localhost:3000/wells');
    const wells = await response.json();

    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM(),
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([-103.602883, 48.079272]),
            zoom: 6
        })
    });

    const vectorSource = new ol.source.Vector();
    wells.forEach(well => {
        if (Object.keys(JSON.parse(well.latitude.replace(/'/g, '"'))).length == 0 || Object.keys(JSON.parse(well.longitude.replace(/'/g, '"'))).length == 0){
            
        }else{
        latitude = Object.keys(JSON.parse(well.latitude.replace(/'/g, '"')))[0];
        longitude = Object.keys(JSON.parse(well.longitude.replace(/'/g, '"')))[0];

        
        console.log(well);
        const marker = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
            name: well.well_name,
            details: `Mcf_of_gas_produced: ${well.mcf_of_gas_produced}, Oil: ${well.barrels_of_oil_produced} barrels/day`
        });

        marker.setStyle(new ol.style.Style({
            image: new ol.style.Circle({
                radius: 6,
                fill: new ol.style.Fill({ color: 'red' }),
                stroke: new ol.style.Stroke({ color: 'black', width: 2 })
            })
        }));

        vectorSource.addFeature(marker);
    }
    });

    const vectorLayer = new ol.layer.Vector({ source: vectorSource });
    map.addLayer(vectorLayer);

    const popupElement = document.createElement('div');
    popupElement.style.position = 'absolute';
    popupElement.style.background = 'white';
    popupElement.style.padding = '10px';
    popupElement.style.display = 'none';
    document.body.appendChild(popupElement);

    map.on('click', event => {
        const feature = map.forEachFeatureAtPixel(event.pixel, f => f);
        if (feature) {
            popupElement.innerHTML = `<b>${feature.get('name')}</b><br>${feature.get('details')}`;
            popupElement.style.left = `${event.pixel[0]}px`;
            popupElement.style.top = `${event.pixel[1]}px`;
            popupElement.style.display = 'block';
        } else {
            popupElement.style.display = 'none';
        }
    });
}

loadMap();
