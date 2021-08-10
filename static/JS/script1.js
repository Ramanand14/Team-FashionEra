"use strict";

var event = document.getElementById("eve").textContent;
var gender = document.getElementById("gen").getAttribute('value');
var age_group = document.querySelector(".para3");
var size_group = document.querySelector(".para4").value;

console.log(event);
console.log(gender);
console.log(age_group);
console.log(size_group);


//hide the content:



//male outfits:
if (gender == "Male") {
    if (age_group == "Kid") {
        if (size_group == "XS") {
            console.log("Condition check!!!");
        } else if (size_group == "S") {
            console.log("Condition check1!!!");
        } else {
            console.log("Condition check3!!!");
        }
    } else if (age_group == "Teen") {
        if (size_group == "M") {
            console.log("Condition check4!!!");
        } else {
            console.log("Condition check5!!!");
        }
    } else if (age_group == "Young Adult") {
        if (size_group == "L") {
            console.log("Condition check6!!!");
        } else {
            console.log("Condition check7!!!");
        }
    } else {
        if (size_group == "XL") {
            console.log("Condition check8!!!");
        } else {
            console.log("Condition check9!!!");
        }
    }
}
    
//Female outfits:
if (gender == "Male") {
    if (age_group == "Kid") {
        if (size_group == "XS") {
            console.log("Condition check10!!!");
        } else if (size_group == "S") {
            console.log("Condition check11!!!");
        } else {
            console.log("Condition check12!!!");
        }
    } else if (age_group == "Teen") {
        if (size_group == "M") {
            console.log("Condition check13!!!");
        } else {
            console.log("Condition check14!!!");
        }
    } else if (age_group == "Young Adult") {
        if (size_group == "L") {
            console.log("Condition check15!!!");
        } else {
            console.log("Condition check16!!!");
        }
    } else {
        if (size_group == "XL") {
            console.log("Condition check17!!!");
        } else {
            console.log("Condition check18!!!");
        }
    }
}