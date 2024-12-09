<script>
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Меню</a>
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
            <li class="nav-item">
              <router-link class="nav-link" to="/">Персонажи</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/content">Контент</router-link>
            </li>
            <li class="nav-item dropdown">
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
</style>