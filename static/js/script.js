async function buscarPokemon() {
    const nomePokemon = document.getElementById("pokemonInput").value.trim();
    if (!nomePokemon) {
      alert("Digite um nome ou número de Pokémon!");
      return;
    }
    
    const url = `/api/pokemon?nomePokemon=${encodeURIComponent(nomePokemon)}`;
  
    try {
      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || "Não foi possível buscar este Pokémon.");
        return;
      }
      
      const data = await response.json();
      exibirPokemon(data);
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Ocorreu um erro ao buscar o Pokémon.");
    }
  }
  
  function exibirPokemon(data) {
    const divResultados = document.getElementById("resultados");
    divResultados.innerHTML = "";
    
    const nomeEl = document.createElement("h2");
    nomeEl.textContent = `${data.nome.toUpperCase()} (ID: ${data.id})`;
    
    const imgEl = document.createElement("img");
    imgEl.src = data.imagem;
    imgEl.alt = data.nome;
    imgEl.classList.add("pokemon-image");
    
    const tiposEl = document.createElement("p");
    tiposEl.textContent = `Tipo(s): ${data.tipos.join(", ")}`;
  
    // Stats como lista
    const statsHeader = document.createElement("p");
    statsHeader.textContent = "Stats:";
    const statsList = document.createElement("ul");
    for (let statName in data.stats) {
      const statItem = document.createElement("li");
      statItem.textContent = `${statName}: ${data.stats[statName]}`;
      statsList.appendChild(statItem);
    }
  
    // Habilidades
    const habEl = document.createElement("p");
    habEl.textContent = `Habilidades: ${data.habilidades.join(", ")}`;
    
    // Evoluções
    const evolucaoEl = document.createElement("p");
    if (data.cadeia_evolutiva.length > 1) {
      evolucaoEl.textContent = "Evoluções: " + data.cadeia_evolutiva.map(n => n.toUpperCase()).join(" -> ");
    } else {
      evolucaoEl.textContent = `${data.nome.toUpperCase()} não evolui (ou não há dados de evolução).`;
    }
    
    divResultados.appendChild(nomeEl);
    divResultados.appendChild(imgEl);
    divResultados.appendChild(tiposEl);
    divResultados.appendChild(statsHeader);
    divResultados.appendChild(statsList);
    divResultados.appendChild(habEl);
    divResultados.appendChild(evolucaoEl);
  }
  