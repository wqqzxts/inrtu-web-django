<script setup>
import { onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

import { storeToRefs } from "pinia";
import useUserStore from "@/stores/userStore";

const userStore = useUserStore();
const { isSuperUser, isAuthenticated, username, userId } =
  storeToRefs(userStore);

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
            src="/Site-logo.png"
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
                    >Роли персонажей</router-link
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
        <form class="d-flex">
          <ul class="navbar-nav">
            <div style="align-content: center;">
              <li class="nav-item dropdown" style="margin-right: 50px">
                <a>
                  {{ username }}
                </a>
              </li>
            </div>
          </ul>
          <router-link class="nav-link" to="/users">
            <button class="btn btn-outline-info" type="button">
              <i class="bi bi-person-fill"></i>
            </button>
          </router-link>
        </form>
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
