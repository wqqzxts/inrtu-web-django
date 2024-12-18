<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const characters = ref([]);
const teams = ref([]);
const positions = ref([]);
const skills = ref([]);
const charactersPictureRef = ref();
const characterAddImageURL = ref();

const characterToAdd = ref({});
const characterToEdit = ref({});

const teamByID = computed(() => {
  return _.keyBy(teams.value, (x) => x.id);
});

const positionByID = computed(() => {
  return _.keyBy(positions.value, (x) => x.id);
});

const skillByID = computed(() => {
  return _.keyBy(skills.value, (x) => x.id);
});

const showZoomImageContainer = ref(false);
const zoomImageUrl = ref("");

function showZoomImage(imageUrl) {
  zoomImageUrl.value = imageUrl;
  showZoomImageContainer.value = true;
}

function hideZoomImage() {
  showZoomImageContainer.value = false;
}
///////////////////////////////////////////////////////////////////////
async function onCharacterAdd() {
  const formData = new FormData();

  formData.append("picture", charactersPictureRef.value.files[0]);

  formData.set("name", characterToAdd.value.name);
  formData.set("team", characterToAdd.value.team);
  formData.set("position", characterToAdd.value.position);
  formData.set("skill", characterToAdd.value.skill);

  await axios.post("/api/characters/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchCharacters();
}

async function charactersAddPictureChange() {
  characterAddImageURL.value = URL.createObjectURL(
    charactersPictureRef.value.files[0]
  );
}

async function onRemoveClick(character) {
  await axios.delete(`/api/characters/${character.id}/`);
  fetchCharacters();
}

async function onCharacterEditClick(character) {
  characterToEdit.value = { ...character };
}

async function onUpdateCharacter() {
  await axios.patch(`/api/characters/${characterToEdit.value.id}/`, {
    ...characterToEdit.value,
  });
  await fetchCharacters();
}
///////////////////////////////////////////////////////////////////////
async function fetchTeams() {
  const r = await axios.get("/api/teams/");
  teams.value = r.data;
}

async function fetchPositions() {
  const r = await axios.get("/api/positions/");
  positions.value = r.data;
}

async function fetchSkills() {
  const r = await axios.get("/api/skills/");
  skills.value = r.data;
}

async function fetchCharacters() {
  const r = await axios.get("/api/characters/");
  characters.value = r.data;
}

onBeforeMount(async () => {
  await fetchCharacters();
  await fetchTeams();
  await fetchPositions();
  await fetchSkills();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onCharacterAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="characterToAdd.name"
                required
              />
              <label for="floatingInput">Имя</label>
            </div>
          </div>

          <div class="col-auto">
            <input
              class="form-control"
              type="file"
              ref="charactersPictureRef"
              @change="charactersAddPictureChange"
              required
            />
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="characterToAdd.team"
                required
              >
                <option :value="t.id" v-for="t in teams" v-bind:key="t.id">
                  {{ t.name }}
                </option>
              </select>
              <label for="floatingInput">Команда</label>
            </div>
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="characterToAdd.position"
                required
              >
                <option :value="p.id" v-for="p in positions" v-bind:key="p.id">
                  {{ p.name }}
                </option>
              </select>
              <label for="floatingInput">Роль</label>
            </div>
          </div>

          <div class="col-auto">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="characterToAdd.skill"
                required
              >
                <option :value="s.id" v-for="s in skills" v-bind:key="s.id">
                  {{ s.name }}
                </option>
              </select>
              <label for="floatingInput">Способность</label>
            </div>
          </div>

          <div class="col-auto" style="align-content: center">
            <button class="btn btn-outline-success btn-lg">
              <i class="bi bi-database-fill-add"></i>
            </button>
          </div>
        </div>
      </form>

      <div>
        <div
          v-for="item in characters"
          class="character-item"
          v-bind:key="item"
        >
          <div>{{ item.name }}</div>
          <div>{{ teamByID[item.team]?.name }}</div>
          <div>{{ positionByID[item.position]?.name }}</div>
          <div>{{ skillByID[item.skill]?.name }}</div>
          <img
            :src="item.picture"
            style="max-height: 60px; cursor: pointer"
            @click="showZoomImage(item.picture)"
          />
          <button
            class="btn btn-outline-primary"
            @click="onCharacterEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editCharacterModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>

      <div class="modal fade" id="editCharacterModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать персонажа
              </h1>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="col-4">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control"
                      v-model="characterToEdit.name"
                    />
                    <label for="floatingInput">Имя</label>
                  </div>
                </div>

                <div class="col-2">
                  <div class="form-floating">
                    <select class="form-select" v-model="characterToEdit.team">
                      <option
                        :value="t.id"
                        v-for="t in teams"
                        v-bind:key="t.id"
                      >
                        {{ t.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Команда</label>
                  </div>
                </div>

                <div class="col-2">
                  <div class="form-floating">
                    <select
                      class="form-select"
                      v-model="characterToEdit.position"
                    >
                      <option
                        :value="p.id"
                        v-for="p in positions"
                        v-bind:key="p.id"
                      >
                        {{ p.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Роль</label>
                  </div>
                </div>

                <div class="col-4">
                  <div class="form-floating">
                    <select class="form-select" v-model="characterToEdit.skill">
                      <option
                        :value="s.id"
                        v-for="s in skills"
                        v-bind:key="s.id"
                      >
                        {{ s.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Способность</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-dismiss="modal"
              >
                <i class="bi bi-x-square-fill"></i>
              </button>
              <button
                data-bs-dismiss="modal"
                type="button"
                class="btn btn-outline-success"
                @click="onUpdateCharacter"
              >
                <i class="bi bi-floppy2-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="zoom-image-container"
      :class="{ active: showZoomImageContainer }"
      @click="hideZoomImage"
    >
      <img :src="zoomImageUrl" alt="Увеличенное изображение" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.character-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}

.custom-modal-width {
  max-width: 1000px;
  width: 900px;
  max-height: 90vh;
  overflow-y: auto;
}

.zoom-image-container {
  position: fixed;
  left: 0;
  top: 40px;
  right: 0;
  bottom: 0;
  display: block;
  padding: 1rem;
  backdrop-filter: blur(4px);
  z-index: 100;
  transform: scale(0.2, 0.2);
  transition: all 0.2s ease-out;
  opacity: 0;
  height: 0;
  overflow: hidden;
}

.zoom-image-container.active {
  opacity: 1;
  transform: scale(1, 1);
  height: auto;
}

.zoom-image-container img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>
