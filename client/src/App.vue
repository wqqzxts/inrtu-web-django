<script setup>
import { onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-xxl p-3 background-filler">
      <div class="container-fluid">
        <a class="navbar-brand">
          <img
            src="Z:\Qzxts\Education\.INRTU\(Code) WEB-Программирование\ВторойСеместр\templates\Site-logo.png"
            alt="Меню"
            width="135"
            height="30"
            class="d-inline-block align-text-top"
          />
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item content-subitem">
              <router-link class="nav-link" to="/">Персонажи</router-link>
            </li>
            <li class="nav-item content-subitem">
              <router-link class="nav-link" to="/content">Контент</router-link>
            </li>
            <li class="nav-item dropdown content-subitem">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Еще
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/teams"
                    >Команды</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/positions"
                    >Роли</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/skills"
                    >Способности</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/content_type"
                    >Тип контента</router-link
                  >
                </li>
                <li>
                  <a class="dropdown-item" href="/admin" target="_blank"
                    >Админка</a
                  >
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style scoped>
.background-filler {
  border: solid 2px #7790b8;
  background-color: #e7eef9;
  border-radius: 6px;  
}

.content-subitem {
  background-color: #fefef9;
  border-radius: 6px;
  border: solid 2px #7790b8;
  padding: 2.5px;
  margin: 2.5px;
}
</style>