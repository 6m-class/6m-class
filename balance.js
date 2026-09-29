let userBalances={};
function initBalances(){const s=localStorage.getItem('user_balances');if(s){try{userBalances=JSON.parse(s);}catch(e){userBalances={};}}}
function saveBalances(){localStorage.setItem('user_balances',JSON.stringify(userBalances));}
function getCurrentUser(){return localStorage.getItem('class_user')||'guest';}
function getUserBalance(){const u=getCurrentUser();if(!userBalances[u])userBalances[u]=100;return userBalances[u];}
function setUserBalance(v){const u=getCurrentUser();userBalances[u]=v;saveBalances();}
function addUserBalance(v){const u=getCurrentUser();if(!userBalances[u])userBalances[u]=100;userBalances[u]+=v;saveBalances();return userBalances[u];}
function deductUserBalance(v){const u=getCurrentUser();if(!userBalances[u])userBalances[u]=100;userBalances[u]-=v;if(userBalances[u]<0)userBalances[u]=0;saveBalances();return userBalances[u];}
initBalances();
