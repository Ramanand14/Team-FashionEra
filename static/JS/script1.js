var event = document.getElementById("Event");
var gender = document.getElementById("Gender");
var age_group = document.getElementById("Age_Group");
var size_group = document.getElementById("Size_Group");

console.log(event);
console.log(gender);
console.log(age_group);
console.log(size_group);

//hide the content:
document.getElementById("Event").style.display = "None";
document.getElementById("Gender").style.display = "None";
document.getElementById("Age_Group").style.display = "None";
document.getElementById("Size_Group").style.display = "None";

//male outfits:
if (gender == "Male"){
    if (age_group == "Kid"){
        if (size_group == "XS"){
            console.log("Condition check!!!");
        }
        else if (size_group == "S"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else if(age_group == "Teen"){
        if (size_group == "M"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else if(age_group == "Young Adult"){
        if (size_group == "L"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else{
        if (size_group == "XL"){
            //stmt
        }
        else{
            //stmt
        }
    }
}
    
//Female outfits:
if (gender == "Male"){
    if (age_group == "Kid"){
        if (size_group == "XS"){
            //stmt
        }
        else if (size_group == "S"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else if(age_group == "Teen"){
        if (size_group == "M"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else if(age_group == "Young Adult"){
        if (size_group == "L"){
            //stmt
        }
        else{
            //stmt
        }
    }
    else{
        if (size_group == "XL"){
            //stmt
        }
        else{
            //stmt
        }
    }
}