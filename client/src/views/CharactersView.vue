<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const characters = ref([]);
const teams = ref([]);
const positions = ref([]);
const skills = ref([]);
const charactersPictureRefAdd = ref();
const charactersPictureRefEdit = ref();
const modalPictureRef = ref("");
const characterAddImageURL = ref();
const characterEditImageURL = ref();

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
///////////////////////////////////////////////////////////////////////
async function onCharacterAdd() {
  const formData = new FormData();

  formData.append("picture", charactersPictureRefAdd.value.files[0]);

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
    charactersPictureRefAdd.value.files[0]
  );
}

async function charactersEditPictureChange() {
  characterEditImageURL.value = URL.createObjectURL(
    charactersPictureRefEdit.value.files[0]
  );
}

async function onRemoveClick(character) {
  await axios.delete(`/api/characters/${character.id}/`);
  fetchCharacters();
}

async function onCharacterEditClick(character) {
  characterToEdit.value = { ...character };
}

async function onImageClick(picture) {
  modalPictureRef.value = picture;
}

async function onUpdateCharacter() {
  const formData = new FormData();

  formData.append("picture", charactersPictureRefEdit.value.files[0]);

  formData.set("name", characterToEdit.value.name);
  formData.set("team", characterToEdit.value.team);
  formData.set("position", characterToEdit.value.position);
  formData.set("skill", characterToEdit.value.skill);

  await axios.patch(`/api/characters/${characterToEdit.value.id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
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
  await fetchTeams();
  await fetchPositions();
  await fetchSkills();
  await fetchCharacters();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onCharacterAdd">
        <div class="row custom-row">
          <div class="my-1 col-12 col-md">
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

          <div class="my-1 col-12 col-md">
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

          <div class="my-1 col-12 col-md">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="characterToAdd.position"
                required
              >
                <option :value="t.id" v-for="t in positions" v-bind:key="t.id">
                  {{ t.name }}
                </option>
              </select>
              <label for="floatingInput">Позиция</label>
            </div>
          </div>

          <div class="my-1 col-12 col-md">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="characterToAdd.skill"
                required
              >
                <option :value="t.id" v-for="t in skills" v-bind:key="t.id">
                  {{ t.name }}
                </option>
              </select>
              <label for="floatingInput">Способность</label>
            </div>
          </div>

          <div class="my-1 col-12 col-md-1" style="align-content: center">
            <input
              class="form-control"
              type="file"
              ref="charactersPictureRefAdd"
              @change="charactersAddPictureChange"
              required
            />
          </div>

          <div class="my-1 col-12 col-md-auto">
            <div
              style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
              "
            >
              <button class="btn btn-outline-success btn-lg">
                <i class="bi bi-database-fill-add"></i>
              </button>
            </div>
          </div>
        </div>
      </form>

      <div
        v-for="item in characters"
        :key="item.id"
        class="row-auto content-item"
      >
        <div>{{ item.name }}</div>
        <div class="content-subitem">
          {{ teamByID[item.team]?.name }}
        </div>
        <div class="content-subitem">
          {{ positionByID[item.position]?.name }}
        </div>
        <div class="content-subitem">
          {{ skillByID[item.skill]?.name }}
        </div>
        <div>
          <img
            :src="item.picture"
            style="max-height: 58px; cursor: zoom-in"
            @click="onImageClick(item.picture)"
            data-bs-toggle="modal"
            data-bs-target="#imageContentModal"
          />
        </div>
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

      <div class="modal fade" id="editCharacterModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать персонажа
              </h1>
            </div>
            <div class="modal-body">
              <div class="col">
                <div class="row">
                  <div class="col">
                    <div class="col-auto">
                      <form
                        class="form-floating"
                        @submit.prevent.stop="onUpdateCharacter"
                      >
                        <input
                          type="text"
                          class="form-control"
                          id="floatingInputValue"
                          v-model="characterToEdit.name"
                          required
                        />
                        <label for="floatingInputValue">Имя</label>
                      </form>
                    </div>
                  </div>
                  
                  <div class="col">
                    <div class="col-auto">
                      <div class="form-floating">
                        <select class="form-select" id="floatingSelect">
                          <option
                            selected
                            :value="t.id"
                            v-for="t in teams"
                            v-bind:key="t.id"
                          >
                            {{ t.name }}
                          </option>
                        </select>
                        <label for="floatingSelect">Команда</label>
                      </div>
                    </div>
                  </div>

                  <div class="col">
                    <div class="col-auto">
                      <div class="form-floating">
                        <select class="form-select" id="floatingSelect">
                          <option
                            selected
                            :value="t.id"
                            v-for="t in positions"
                            v-bind:key="t.id"
                          >
                            {{ t.name }}
                          </option>
                        </select>
                        <label for="floatingSelect">Позиция</label>
                      </div>
                    </div>
                  </div>

                  <div class="col">
                    <div class="col-auto">
                      <div class="form-floating">
                        <select class="form-select" id="floatingSelect">
                          <option
                            selected
                            :value="t.id"
                            v-for="t in skills"
                            v-bind:key="t.id"
                          >
                            {{ t.name }}
                          </option>
                        </select>
                        <label for="floatingSelect">Способность</label>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="row my-2">
                  <div class="my-1" style="align-content: center">
                    <input
                      class="form-control"
                      type="file"
                      ref="charactersPictureRefEdit"
                      @change="charactersEditPictureChange"
                      required
                    />
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

      <div class="modal fade" id="imageContentModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                Изображение
              </h1>
            </div>
            <div class="modal-body">
              <img
                :src="modalPictureRef"
                class="img-fluid"
                alt="Увеличенное изображение"
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-dismiss="modal"
              >
                <i class="bi bi-x-square-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content-item {
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

.content-subitem {
  background-color: #cee1f9;
  border-radius: 5px;
  padding: 10px;
}

@media (max-width: 1500px) {
  .custom-row > div {
    flex: 0 0 auto;
    max-width: auto;
  }
}

.content-item {
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

@media (max-width: 1000px) {
  .content-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .content-item > div,
  .content-item img,
  .content-item button {
    width: 100%;
    text-align: center;
    margin: 5px 0;
  }

  .content-item img {
    max-height: auto;
    margin-top: 10px;
  }
}
</style>
