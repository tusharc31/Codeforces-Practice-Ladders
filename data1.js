const fetch = require("node-fetch");
// import { uid } from "./config";
// import { srat } from "./config";
// import { erat } from "./config";
// 
// const username = uid()
// const starting_rating = srat()
// const ending_rating = erat()
// 
// console.log(username)
// console.log(starting_rating)
// console.log(ending_rating)

// console.log(fetch('https://codeforces.com/api/contest.list'));

const qlist=[];
async function getQuestions() {
    let response = await fetch('https://codeforces.com/api/contest.list');
    let data = await response.json()
    return data;
}

data = getQuestions()
// .then(data => qlist=data['result']);
// getQuestions().then(data => console.log(data['result']));
console.log(data);