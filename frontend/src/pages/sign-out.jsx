import {useEffect, useState} from "react";

export default function SignOut(page) {


    useEffect(() => {
        fetch("/sign-out", {method: 'GET'})
            .then(res => res)
            .then(data => {
                console.log(data);
            })
    }, [])
}