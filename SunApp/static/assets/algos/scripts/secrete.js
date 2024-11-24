// Empêcher de voire les codes sources
const disabledKeys = [ "c" , "C" , "x" , "J" , "u" , "I" ]; // touches qui seront désactivées

const showAlert = e => { 
e. preventDefault(); // empêche son comportement par défaut
return alert ( "Désolé, vous n'êtes pas autorisés !" ); 
}

document. addEventListener ( "contextmenu" , e => { 
showAlert(e) ; // appel de la fonction showAlert() au clic droit de la souris
}) ;

document. addEventListener ( "keydown" , e => { 
// appel de la fonction showAlert(), si la touche enfoncée correspond aux touches désactivées
if ((e. ctrlKey && disabledKeys. includes ( e. key )) || e. key === "F12" ) {   
    showAlert(e);
}
});